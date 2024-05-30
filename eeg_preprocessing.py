import os
import json
import pickle
import argparse
import numpy as np
import torch

from tqdm import tqdm

from src import read_config
from src.preprocessing import z_score_standardization, add_white_gaussian_noise, rbf_interpolation


def parse_args():
    """
    Parameters required for learning can be specified when executing the file.
    """
    
    parser = argparse.ArgumentParser(description = 'Noise Add Process at EEG')
    
    parser.add_argument(
        "--data_path",
        type = str,
        default = "data/EEG_ImageNet/original/eeg_5_95_std.npy",
        help = "EEG data path"
    )
    parser.add_argument(
        "--snr_ratio",
        type = float,
        default = 10,
        help = "Signal to Noise Ratio"
    )
    parser.add_argument(
        "--interpolate",
        type = str,
        default = "linear",
        help = "Interpolation function"
    )
    parser.add_argument(
        "--smooth",
        type = float,
        default = 0.,
        help = "Smoothing Coefficient"
    )
    parser.add_argument(
        "--save_path",
        type = str,
        help = "Save path"
    )
    
    args = parser.parse_args()
    return args


def data_split(data, split_ratio = [0.6, 0.2, 0.2]):
    """
    Create an index standard to split the dataset into "train", "valid", and "test" purposes.
    """
    n_data = data.shape[0]
    
    split_index = []
    
    for i, ratio in enumerate(split_ratio[:-1]):
        if i == 0:
            split_index.append(int(n_data * ratio))
        else:
            split_index.append(split_index[0] + int(n_data * ratio))
    return split_index


if __name__ == "__main__":
    np.random.seed(42)
    
    args = parse_args()
    
    # Select 8-channel Name & Order Information
    ch_order = read_config(path = "data/eegmmidb/ch_order.json")
    montage  = read_config(path = "data/Montage/64_ch_system.pkl")
    
    selected_channels = list(ch_order.values())
    ch_order_list = list(ch_order.keys())
    
    # Get channel's position coordinates
    positions = montage.get_positions()['ch_pos']
    selected_positions = np.array([positions[ch] for ch in selected_channels])
    all_positions = np.array([positions[ch] for ch in montage.ch_names if ch in positions])  
    
    eeg_data = np.load(args.data_path)
    split_index = [13254] # data_split(eeg_data, [0.6, 0.2, 0.2])
    
    if len(split_index) == 2:
        save_dict = {
            "LR": {"train": [], "valid": [], "test": []},
            "HR": {"train": [], "valid": [], "test": []}
        }
    elif len(split_index) == 1:
        save_dict = {
            "LR": {"train": [], "test": []},
            "HR": {"train": [], "test": []}
        }
    
    print("====EEG data Preprocessing Process====")
    for idx in tqdm(range(eeg_data.shape[0])):
        sample = z_score_standardization(eeg_data[idx])
        
        # Add noise based on given SNR ratio
        if args.snr_ratio != 0:
            noise_sample = add_white_gaussian_noise(sample, args.snr_ratio)
            
            select_8_sample = np.concatenate(
                [noise_sample[int(ch_idx)].reshape(1, -1) for ch_idx in ch_order_list],
                axis = 0
            )
        else:
            # 8 channel selection
            ## “interpolate” in pytorch requires Batch and Channel dimensions, so add those dimensions.
            select_8_sample = np.concatenate(
                [sample[int(ch_idx), :].reshape(1, -1) for ch_idx in ch_order_list],
                axis = 0
            )
            
        # Make 128 channels of low resolution EEG data by applying “Bicubic” interpolation
        interp_sample = rbf_interpolation(
            select_8_sample,
            selected_positions,
            all_positions,
            args.interpolate,
            smooth = args.smooth
        )
        
        lr_data = torch.FloatTensor(interp_sample).view(1, 1, *interp_sample.shape)
        hr_data = torch.FloatTensor(sample).view(1, 1, *sample.shape)
        
        # Change the list to contain data according to the split index
        if len(split_index) == 2:
            if idx < split_index[0]:
                save_dict["LR"]["train"].append(lr_data)
                save_dict["HR"]["train"].append(hr_data)
            elif idx < split_index[1]:
                save_dict["LR"]["valid"].append(lr_data)
                save_dict["HR"]["valid"].append(hr_data)
            else:
                save_dict["LR"]["test"].append(lr_data)
                save_dict["HR"]["test"].append(hr_data)
        elif len(split_index) == 1:
            if idx < split_index[0]:
                save_dict["LR"]["train"].append(lr_data)
                save_dict["HR"]["train"].append(hr_data)
            else:
                save_dict["LR"]["test"].append(lr_data)
                save_dict["HR"]["test"].append(hr_data)
    
    # Save 
    torch.save(save_dict, args.save_path)
    print("Preprocessing finish!!")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    