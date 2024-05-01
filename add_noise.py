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


def data_split(data, split_ratio = [0.6, 0.2, 0.2]):
    """
    Create an index standard to split the dataset into "train", "valid", and "test" purposes.
    """
    n_data = len(data)
    
    split_index = []
    
    for i, ratio in enumerate(split_ratio[:-1]):
        if i == 0:
            split_index.append(int(n_data * ratio))
        else:
            split_index.append(split_index[0] + int(n_data * ratio))
    return split_index


if __name__ == "__main__":
    
    args = parse_args()
    
    with open("data/EEG_ImageNet/ch_order.json", "r") as f:
        ch_order = json.load(f)
    
    # Selected 8-Channel Order Information
    ch_order_list = list(ch_order.keys())

    eeg_data = torch.load(args.data_path)["dataset"]
    split_index = data_split(eeg_data)

    data_dict = {
        "LR": {
            "train": [],
            "valid": [],
            "test": []
        },
        "HR": {
            "train": [],
            "valid": [],
            "test": []
        }
    }
    
    for idx in tqdm(range(len(eeg_data))):
        # Using only 440 samples, excluding some of the preceding time
        sample = eeg_data[idx]["eeg"].numpy().astype(np.float32)[:, -440:]
        
        # Add noise based on given SNR ratio
        wgn_sample = add_white_gaussian_noise(sample, args.snr_ratio)
        
        # 8 channel selection
        ## “interpolate” in pytorch requires Batch and Channel dimensions, so add those dimensions.
        ## 8 x (1, 1, 1, 440) => Concat => (1, 1, 8, 440)
        wgn_8_sample = torch.cat(
            [wgn_sample[int(i), :].reshape(1, 1, 1, -1) for i in ch_order_list],
            axis = 2
        )
        
        # Make 128 channels of low resolution EEG data by applying “Bicubic” interpolation
        lr_data = interpolate(wgn_8_sample, scale_factor = (16, 1), mode = 'bicubic')
        hr_data = torch.FloatTensor(sample).unsqueeze(0).unsqueeze(0)
        
        # Change the list to contain data according to the split index
        if idx < split_index[0]:
            data_dict["LR"]["train"].append(lr_data)
            data_dict["HR"]["train"].append(hr_data)
        elif idx < split_index[1]:
            data_dict["LR"]["valid"].append(lr_data)
            data_dict["HR"]["valid"].append(hr_data)
        else:
            data_dict["LR"]["test"].append(lr_data)
            data_dict["HR"]["test"].append(hr_data)
    
    # Save
    save_path = args.save_path.split(".")[0] + f"_snr_{args.snr_ratio}.pth"   
    torch.save(data_dict, save_path)