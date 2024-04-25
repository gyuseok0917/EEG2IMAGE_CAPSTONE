import json
import argparse
import numpy as np
import torch

from tqdm import tqdm
from torch.nn.functional import interpolate

from src import add_white_gaussian_noise, add_real_noise


def parse_args():
    """
    Parameters required for learning can be specified when executing the file.
    """
    
    parser = argparse.ArgumentParser(description = 'Noise Add Process at EEG')
    
    parser.add_argument(
        "--data_path",
        type = str,
        default = "data/EEG_ImageNet/original/eeg_5_95_std.pth", help = "EEG data path"
    )
    parser.add_argument(
        "--snr_ratio",
        type = float,
        help = "Signal to Noise Ratio"
    )
    parser.add_argument(
        "--save_path",
        type = str,
        default = "data/EEG_ImageNet/preprocessing/5-95/eeg_5_95_std_dataset.pth", help = "Save path"
    )
    
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    
    args = parse_args()
    
    with open("data/EEG_ImageNet/ch_order.json", "r") as f:
        ch_order = json.load(f)
    
    # Selected 8-Channel Order Information
    ch_order_list = list(ch_order.keys())

    eeg_data = torch.load(args.data_path)["dataset"]

    # Dataset object to save
    data_dict = {
        "LR": [],
        "HR": []
    }
    
    for idx in tqdm(range(len(eeg_data))):
        sample = eeg_data[idx]["eeg"].numpy().astype(np.float32)
        
        wgn_sample = add_white_gaussian_noise(sample, args.snr_ratio)
        
        wgn_8_sample = torch.cat(
            [wgn_sample[int(i), :].reshape(1, 1, 1, -1) for i in ch_order_list],
            axis = 2
        )
        
        lr_data = interpolate(wgn_8_sample, scale_factor = (16, 1), mode = 'bicubic')
        hr_data = torch.FloatTensor(sample)
        
        data_dict["LR"].append(lr_data)
        data_dict["HR"].append(hr_data)
    
    save_path = args.save_path.split(".")[0] + f"_snr_{args.snr_ratio}.pth"
    print(save_path)
    
    torch.save(data_dict, save_path)