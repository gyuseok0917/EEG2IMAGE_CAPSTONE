import os
import json
import argparse
import pandas as pd
import torch
import torch.backends.cudnn as cudnn

from tqdm import tqdm
from torch.nn import MSELoss
from torch.optim import Adam

# from src.train import NMSELoss
from src import GetLoader
from src.model import DeepCNN
from src.train import Meter, LossMeter, MetricMeter
from src.train import signal_to_noise_ratio, pearson_correlation_coefficient
from src.train import make_dirs, set_logging, TensorBoradSummary, EarlyStoping


def parse_args():
    """
    Parameters required for learning can be specified when executing the file.
    """
    parser = argparse.ArgumentParser(description = 'DeepCNN Train')
    
    parser.add_argument('--GPU_NUM', type = int, help = "GPU Index Num will use")
    parser.add_argument("--SEED", type = bool, help = "Whether seed is set or not")
    parser.add_argument('--data_path', type = str, help = 'input data(eeg) path')
    parser.add_argument('--ckpt_dir', type = str, help = 'checkpoint save folder')
    parser.add_argument('--log_dir', type = str, help = 'Logging inform save folder')
    parser.add_argument('--interval', type = int, help = "Train log monitering step")
    parser.add_argument('--epochs', type = int, help = 'Number of epochs to train')
    parser.add_argument('--batch_size', type = int, help = 'Input batch size for training')
    parser.add_argument('--learning_rate', type=float, help='learning rate')
    args = parser.parse_args()
    return args


def train_step(
    model,
    dataloader,
    criterion,
    optimizer,
    interval,
    iters,
    device
):
    total_meter = Meter()
    loss_meter = LossMeter(criterion)
    snr_meter = MetricMeter(metric["SNR"])
    pcc_meter = MetricMeter(metric["PCC"])
    
    # train mode
    model.train()
    
    logger.info("==========Train==========")
    for lr_eeg, hr_eeg in dataloader:
        lr_eeg = lr_eeg.to(device)
        hr_eeg = hr_eeg.to(device)
        batch_size = lr_eeg.size(0)
        
        # Optimizer initializing
        optimizer.zero_grad()
        
        sr_eeg = model(lr_eeg)
        
        # Log value Update & backward
        total_meter.update(batch_size)
        loss_meter.calculate(sr_eeg, hr_eeg)
        snr_meter.calculate(sr_eeg, hr_eeg)
        pcc_meter.calculate(sr_eeg, hr_eeg)
        optimizer.step()
        
        if total_meter.value() % interval == 0:
            
            logger.info(f"Epoch {iters + 1:>3} [{int(total_meter.value()):>4}/{len(dataloader.dataset)}]")
            logger.info("--------------------------")
            logger.info(f"Loss ==> {loss_meter.value():.5f}")
            logger.info(f"SNR  ==> {snr_meter.value():>3.2f}")
            logger.info(f"PCC  ==> {pcc_meter.value():.3f}")
            logger.info("--------------------------\n")
            
    return loss_meter.value(), snr_meter.value(), pcc_meter.value()


@torch.no_grad()
def test_step(
    model,
    dataloader,
    criterion,
    device
):
    loss_meter = LossMeter(criterion)
    snr_meter = MetricMeter(metric["SNR"])
    pcc_meter = MetricMeter(metric["PCC"])
    
    # test mode
    model.eval()
    
    logger.info("========Evaluation========")
    for lr_eeg, hr_eeg in tqdm(dataloader):
        lr_eeg = lr_eeg.to(device)
        hr_eeg = hr_eeg.to(device)
        
        sr_eeg = model(lr_eeg)
        
        # Loss & Metric value calculation
        loss_meter.calculate(sr_eeg, hr_eeg)
        snr_meter.calculate(sr_eeg, hr_eeg)
        pcc_meter.calculate(sr_eeg, hr_eeg)
        
    return loss_meter.value(), snr_meter.value(), pcc_meter.value()


def main(
    model,
    train_loader,
    valid_loader,
    criterion,
    optimizer,
    interval,
    max_iters,
    ckpt_dir,
    log_dir,
    patience,
    device
):
    # earlystoping
    early_stoper = EarlyStoping(
        path = os.path.join(ckpt_dir, "model.pt"),
        logging = logger,
        patience = patience,
        verbose = True
    )
    
    # Tensorboard
    tensorboard = TensorBoradSummary(log_dir)
    
    
    for iters in range(max_iters):
        
        # train
        train_loss, train_snr, train_pcc = train_step(
            model, train_loader, criterion, optimizer, metric, iters, interval, device
        )
        
        # validation
        valid_loss, valid_snr, valid_pcc = test_step(
            model, valid_loader, criterion, metric, device
        )
        
        logger.info("--------------------------")
        logger.info(f"Loss ==> {valid_loss:.5f}")
        logger.info(f"SNR  ==> {valid_snr:>3.2f}")
        logger.info(f"PCC  ==> {valid_pcc:.3f}")
        logger.info("--------------------------\n")
        
        # Update checkpoint file when verification loss value decreases
        early_stoper(valid_loss, model)
        
        # If there is no progress in performance improvement equal to the number of patients,
        # learning is forced to stop.
        if early_stoper.early_stop:
            break
        
        # tensorboard log save
        board_dict = {
            "Loss/train": train_loss,
            "SNR/train": train_snr,
            "PCC/valid": train_pcc,
            "Loss/valid": valid_loss,
            "SNR/valid": valid_snr,
            "PCC/valid": valid_pcc,
            "step": iters
        }
        
        tensorboard(board_dict)
    
    # tensorboard process & logging finish
    tensorboard.flush()
    tensorboard.close()
    logger.shutdown()
  
        
if __name__ == "__main__":
    
    args = parse_args()
    
    # Environment Setting
    if args.SEED:
        torch.manual_seed(42)
    device = f"cuda:{args.GPU_NUM}"
    cudnn.benchmark = True
    
    PATIENCE = 8
    
    # create save directory
    make_dirs([args.ckpt_dir, args.log_dir])
    
    # Create logging object
    global logger
    logger = set_logging(args.log_dir, "log.txt")
    
    train_loader, valid_loader = GetLoader(
        args.data_path,
        dataset_mode = ["train", "valid"],
        batch_size = args.batch_size,
        shuffle = True,
        pin_memory = True,
        num_workers = 2
    )
    
    # Model set
    model = DeepCNN().to(device)
    
    criterion = MSELoss()
    optimizer = Adam(model.parameters(), lr = args.leraning_rate)
    
    metric = {
        "SNR": signal_to_noise_ratio,
        "PCC": pearson_correlation_coefficient
    }
    
    main(
        model = model,
        train_loader = train_loader,
        train_loader = train_loader,
        criterion = criterion,
        optimizer = optimizer,
        interval = args.interval,
        max_iters = args.epochs,
        ckpt_dir = args.ckpt_dir,
        log_dir = args.log_dir,
        patience = PATIENCE,
        device = device
    )
    
    
        
        








