import torch
import torch.nn as nn
import torch.nn.functional as F


class DeepCNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Encoder Module
        self.en_module = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size = (13, 5), stride = 2, padding = 1),
            nn.PReLU(),
            nn.Conv2d(64, 64, kernel_size = (13, 5), stride = 2, padding = 1),
            nn.PReLU(),
            nn.Conv2d(64, 64, kernel_size = (13, 5), stride = 2, padding = 1),
            nn.PReLU()
        )
        
        # Decoder Module
        self.de_module = nn.Sequential(
            nn.ConvTranspose2d(64, 64, kernel_size = (13, 9), stride = 2, padding = 1, output_padding = 1),
            nn.PReLU(),
            nn.ConvTranspose2d(64, 64, kernel_size = (13, 9), stride = 2, padding = 1, output_padding = 1),
            nn.PReLU(),
            nn.ConvTranspose2d(64, 64, kernel_size = (13, 9), stride = 2, padding = 1, output_padding = 1),
            nn.PReLU(),
            nn.Conv2d(64, 64, kernel_size = (13, 5), stride = 1, padding = 1),
            nn.PReLU(),
            nn.Conv2d(64, 1, kernel_size = (7, 1), stride = 1, padding = 1),
            nn.PReLU()
        )

    
    def forward(self, inputs):
        out = self.en_module(inputs)    # Encoder Process
        out = self.de_module(out)       # Decoder process
        return out
