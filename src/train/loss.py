import torch
from torch.nn import Module, MSELoss


class NMSELoss(Module):
    """
    Function to calculate the NMSE
    
    NMSE = MNSE(P, Y) / (Y_max - T_min)
    """
    def __init__(self):
        super().__init__()
        
        self.mse = MSELoss() 
        
    def forward(self, preds, targets):
        nmse_score = self.mse(preds, targets) / (targets.max() - targets.min())
        return nmse_score