import torch

from typing import Dict, List
from torch.utils.data import Dataset, DataLoader


class EEG_Dataset(Dataset):
    """
    Args:
        eeg_dict (Dict): EEG data organized in dictionary formh
        
        [Structure]
        
        {
            "LR": {
                "train": ...,
                "valid": ...,
                "test": ...
            },
            "HR": {
                "train": ...,
                "valid": ...,
                "test": ...
            }
        }
    """
    def __init__(self, eeg_dict: Dict, mode = "train"):
        
        lr_data = torch.cat(eeg_dict["LR"][mode], axis = 0)
        hr_data = torch.cat(eeg_dict["HR"][mode], axis = 0)
            
    
    def __len__(self):
        return self.lr_data.shape[0]
    
    
    def __getitem__(self, idx):
        return self.lr_data[idx], self.hr_data[idx]
    
    
class GetLoader:
    """
    Class to create dataloader
    
    Args:
        data_path: EEG data's path (format: .pt)
        dataset_mode: Create three types of datasets: “train”, “valid”, and “test”
    """
    def __init__(
        self,
        data_path,
        dataset_mode,
        batch_size,
        shuffle = False,
        pin_memory = False,
        num_workers = 0
    ):
        
        assert type(dataset_mode) == list or type(dataset_mode) == str
        
        self.mode = dataset_mode
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.pin_memory = pin_memory
        self.num_workers = num_workers
        
        # Data Load
        self.eeg_dict = torch.load(data_path)
        
        
    def create_loader(self, mode):
        dataset = EEG_Dataset(self.eeg_dict, mode)
        
        if mode == "valid" or mode == "test":
            self.shuffle = False
        
        dataloader = DataLoader(
            dataset = dataset,
            batch_size = self.batch_size,
            shuffle = self.shuffle,
            pin_memory = self.pin_memory,
            num_workers = self.num_workers,
        )
        
        return dataloader
    
    
    def get_loader(self):
        if type(self.mode) == list:
            loader_list = []
            
            for mode in self.mode:
                loader_list.append(self.create_loader(mode))
            return loader_list
        else:
            return self.create_loader(self.mode)