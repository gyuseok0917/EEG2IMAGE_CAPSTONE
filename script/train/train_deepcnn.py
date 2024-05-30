import os
import sys

workspace = "/workspace"
os.chdir(workspace)
sys.path.append(workspace)

# ===== Module Import =====
import argparse
import oyaml as yaml
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn

from tqdm import tqdm
from torch.optim import Adam, AdamW

from src import GetLoader, read_config
from src.model.deepcnn import DeepCNN
from src.train import signal_to_noise_ratio, pearson_correlation_coefficient, NMSELoss
from src.train import Meter, LossMeter, MetricMeter
from src.train import make_dirs, set_logging, WandbLog, EarlyStoping


# =================================== Training Parser ===================================

parser = argparse.ArgumentParser(description = 'DeepCNN Train')

parser.add_argument('--GPU', type = str, help = "Set the GPU number to use (“multi” for multi-process)")
parser.add_argument("--config_path", type = str, help = "Configuration file path")
parser.add_argument("--wandb_path", type = str, help = "Wandb Configuration path")
parser.add_argument('--data_path', type = str, help = 'input data(eeg) path')
parser.add_argument('--runs_dir', type = str, help = 'checkpoint & log save folder')
parser.add_argument('--interval', type = int, help = "Train log monitering step")
parser.add_argument('--epochs', type = int, help = 'Number of epochs to train')
parser.add_argument('--batch_size', type = int, help = 'Input batch size for training')
parser.add_argument('--learning_rate', type = float, help ='learning rate')
parser.add_argument('--weight_decay', type = float, help = 'weight decay')
args = parser.parse_args()

# =======================================================================================


def train_step(
    model,
    dataloader,
    criterion,
    optimizer,
    metric,
    interval,
    iters,
    mask_channel
):
    total_meter = Meter()
    loss_meter = LossMeter(criterion)
    snr_meter = MetricMeter(metric["SNR"])
    pcc_meter = MetricMeter(metric["PCC"])
    
    # train mode
    model.train()
    
    logger.info("==========Train==========")
    for lr_eeg, hr_eeg in dataloader:
        lr_eeg = lr_eeg.cuda()
        hr_eeg = hr_eeg.cuda()
        batch_size = lr_eeg.size(0)
        
        # Optimizer initializing
        optimizer.zero_grad()
        
        sr_eeg = model(lr_eeg)
#         sr_eeg[..., mask_channel] = hr_eeg[..., mask_channel]

        # Log value Update & backward
        total_meter.update(batch_size)
        loss_meter.calculate(sr_eeg, hr_eeg, mode = "train")
        snr_meter.calculate(sr_eeg, hr_eeg)
        pcc_meter.calculate(sr_eeg, hr_eeg)
        optimizer.step()
        
        if total_meter.value() % interval == 0:
            
            logger.info(f"Epoch {iters + 1:>3} [{int(total_meter.value()):>4}/{len(dataloader.dataset)}]")
            logger.info("--------------------------")
            logger.info(f"Loss ==> {loss_meter.value():.5f}")
            logger.info(f"SNR  ==> {snr_meter.value():>3.3f}")
            logger.info(f"PCC  ==> {pcc_meter.value():.3f}")
            logger.info("--------------------------\n")
            
    return {"Loss/Train": loss_meter.value(), "SNR/Train": snr_meter.value(), "PCC/Train": pcc_meter.value()}


@torch.no_grad()
def valid_step(
    model,
    dataloader,
    criterion,
    metric,
    mask_channel
):
    loss_meter = LossMeter(criterion)
    snr_meter = MetricMeter(metric["SNR"])
    pcc_meter = MetricMeter(metric["PCC"])
    
    # test mode
    model.eval()
    
    logger.info("========Evaluation========")
    for lr_eeg, hr_eeg in tqdm(dataloader):
        lr_eeg = lr_eeg.cuda()
        hr_eeg = hr_eeg.cuda()
        
        sr_eeg = model(lr_eeg)
#         sr_eeg[..., mask_channel] = hr_eeg[..., mask_channel]
        
        # Loss & Metric value calculation
        loss_meter.calculate(sr_eeg, hr_eeg)
        snr_meter.calculate(sr_eeg, hr_eeg)
        pcc_meter.calculate(sr_eeg, hr_eeg)

    return {"Loss/Valid": loss_meter.value(), "SNR/Valid": snr_meter.value(), "PCC/Valid": pcc_meter.value()}


def main(args):
    make_dirs(args.runs_dir)
    
    global logger
    logger = set_logging(os.path.join(args.runs_dir, "log.txt"))
    
    wandb_save_kwargs = read_config(args.wandb_path)
    wandb_obj = WandbLog(wandb_save_kwargs)
    
    org_ch = read_config("data/EEG_ImageNet/ch_order.json")
    mask_channel = [int(ch) for ch in org_ch.keys()]
    
    torch.manual_seed(42)
    cudnn.benchmark = True
    
    model_params_kwargs = read_config(args.config_path)
    model = DeepCNN(model_params_kwargs)
    if args.GPU == "multi":
        model = nn.DataParallel(model)
        model.cuda()
    else:
        os.environ["CUDA_VISIBLE_DEVICES"]=args.GPU
        model.cuda()
        
    criterion = NMSELoss()
#     optimizer = Adam(model.parameters(), lr = args.learning_rate, weight_decay = args.weight_decay)
    optimizer = AdamW(model.parameters(), lr = args.learning_rate, betas = (0.9, 0.95), weight_decay = args.weight_decay)
    
    metric = dict(SNR = signal_to_noise_ratio, PCC = pearson_correlation_coefficient)
        
    train_loader, valid_loader = GetLoader(
        args.data_path,
        dataset_mode = ["train", "test"],
        batch_size = args.batch_size,
        shuffle = True,
        pin_memory = True,
        num_workers = 2
    ).get_loader()
    
    best_score = 0.
    
    for iters in range(args.epochs):
        
        train_log = train_step(model, train_loader, criterion, optimizer, metric, args.interval, iters, mask_channel)
        valid_log = valid_step(model, valid_loader, criterion, metric, mask_channel)
        
        logger.info("--------------------------")
        logger.info(f"Loss ==> {valid_log['Loss/Valid']:.5f}")
        logger.info(f"SNR  ==> {valid_log['SNR/Valid']:>3.3f}")
        logger.info(f"PCC  ==> {valid_log['PCC/Valid']:.3f}")
        logger.info("--------------------------\n")
        
        if iters == 0:
            torch.save(model.state_dict(), os.path.join(args.runs_dir, "model.pt"))
            best_score = valid_log["Loss/Valid"]
            print("Save Checkpoint!")
        else:
            if valid_log["Loss/Valid"] < best_score:
                torch.save(model.state_dict(), os.path.join(args.runs_dir, "model.pt"))
                best_score = valid_log["Loss/Valid"]
                print("Save Checkpoint!")
            else:
                print("Update failed...")
            
        wandb_obj.update({**train_log ,**valid_log}, step = iters)
    
    logger.shutdown()
    wandb_obj.finish()
  
        
if __name__ == "__main__":
    main(args)
    
    
        
        








