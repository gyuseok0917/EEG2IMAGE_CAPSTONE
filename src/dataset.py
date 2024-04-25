import torch

from torch.utils.data import Dataset, DataLoader


class EEG_Dataset(Dataset):
    """
    EEG Dataset
    
    Args:
        data_path: EEG data path (format: pth)
    """
    def __init__(self, data_path, mode = "train"):
        
        data_dict = torch.load(data_path)
        
        self.lr_data = torch.cat(data_dict["LR"], axis = 0)
        self.hr_data = torch.cat(data_dict["HR"], axis = 0)
        
    
    def __len__(self):
        return self.lr_data.shape[0]
    
    
    def __getitem__(self, idx):
        return self.lr_data[idx], self.hr_data[idx]
    
    
def get_dataloader(
    dataset,
    batch_size,
    shuffle = False,
    pin_memory = False,
    num_workers = 0,
    sampler = None
):
    return DataLoader(
        dataset = dataset,
        batch_size = batch_size,
        shuffle = shuffle,
        pin_memory = pin_memory,
        num_workers = num_workers,
        sampler = sampler
    )