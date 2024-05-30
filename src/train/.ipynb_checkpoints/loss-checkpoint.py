import torch
from torch.nn import Module, MSELoss


class MSLELoss(Module):
    """
    Function to calculate the MSLE (Mean Squared Log Error)
    
    MSLE = MSE(log_e(P) - log_e(Y))
    """
    def __init__(self):
        super().__init__()
        
        self.mse = MSELoss()
        
        
    def forward(self, preds, targets):
        msle_score = self.mse(torch.log(preds), torch.log(targets))
        return msle_score


class NMSELoss(Module):
    """
    Function to calculate the NMSE (Normalization Mean Squared Error)
    
    NMSE = MNSE(P, Y) / (Y_max - T_min)
    """
    def __init__(self):
        super().__init__()
        
        self.mse = MSELoss()
        
        
    def forward(self, preds, targets):
        nmse_score = self.mse(preds, targets) / targets.mean()
        return nmse_score