import os
import logging

from typing import List
from torch.utils.tensorboard import SummaryWriter


def make_dirs(dirs: str or List[str]):
    """
    Funtion to create folders.
    
    Args:
        dirs (str or List[str])
    """
    
    # Run only when there is no folder to create
    for dir_root in dirs:
        if os.path.isdir(dir_root) == False:
            os.makedirs(dir_root)
            
            
def set_logging(save_path = None):
    """
    A logging object creation function that will output logs (and other information, etc.)
    to the screen and simultaneously save them to a text file.
    
    Args:
        log_dir (str): Folder path to save log record files
        file_name (str): File name to save
    """
    
    # Check
    assert os.path.isdir(os.path.dirname(save_path)) == True
    assert save_path.split(".")[-1] == "txt"
    
    if save_path == None:
        logging.basicConfig(
            level = logging.INFO,
            format = '%(message)s'
        )
    else:
        logging.basicConfig(
            filename = save_path
        )
    
    # Setting the function to output logs to the screen
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_handler)
    
    return logging


class TensorBoradSummary:
    """
    Functions to use Tensorboard usefully
    """   
    def __init__(self, log_dir):
        
        # tensorboard writer object
        self.writer = SummaryWriter(log_dir = log_dir)
        
        
    def __call__(self, info_dict):
        step = info_dict["step"]
        
        for log_name, log_value in info_dict.items()[:-1]:
            if log_name == "step":
                pass
            else:
                self.writer.add_scalar(log_name, log_value, step)
                
                
class EarlyStoping:
    def __init__(
        self,
        path,
        logging,
        patience: int = 8,
        verbose: bool = False,
        delta: float = 0.
    ):
        """
        Early stops the training if validation loss doesn't improve after a given patience.
        
        Args:
            path (str): Path for the checkpoint to be saved to.
            patience (int): How long to wait after last time validation loss improved.
                            Default: 8
            verbose (bool): If True, prints a message gor each validation loss improvement.
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0.
        """
        self.path = path
        self.patience = patience
        self.logging = logging
        self.verbose = verbose
        self.counter = 0       # number of warnings
        self.best_score = None # Contains the lowest valid loss
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta


    def __call__(self, val_loss, model):
        """
        Parameters:
            val_loss: Current epoch's validation loss
            model: Training model
            num_iter: Current epoch that will monitoring.
                      if loss updated, it will be checkpoint file's first name. 
        """
        score = val_loss
        
        # The first epoch saves the weight immediately.
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        # if valid loss of current epoch > best_score: Add warning count
        elif score > (self.best_score + self.delta):
            self.counter += 1           
            self.logging.info(f'EarlyStopping counter: {self.counter} out of {self.patience} |')
            if self.counter >= self.patience:
                self.early_stop = True
        # if valid loss of current epoch < best_score: Update best score and save weight
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

   
    def save_checkpoint(self, val_loss, model):
        if self.verbose:
            self.logging.info(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ... |')
        # Model's weight save
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss


















