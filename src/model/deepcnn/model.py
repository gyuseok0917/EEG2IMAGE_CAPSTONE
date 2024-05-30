import torch
import torch.nn as nn


class DeepCNN(nn.Module):
    """
    DeepCNN based Denoising Auto encoder
    
    Args:
        params_kwargs: Model parameters's Configuration
    """
    def __init__(self, params_kwargs):
        super().__init__()
        
        # Encoder Block
        self.en_module = nn.Sequential(
            nn.Conv2d(**params_kwargs["encoder"][0]),
            nn.Conv2d(**params_kwargs["encoder"][1]),
            nn.Conv2d(**params_kwargs["encoder"][1])
        )
        
        # Decoder Block
        self.de_module = nn.Sequential(
            nn.ConvTranspose2d(**params_kwargs["decoder"]),
            nn.ConvTranspose2d(**params_kwargs["decoder"]),
            nn.ConvTranspose2d(**params_kwargs["decoder"]),
            nn.ConvTranspose2d(**params_kwargs["output"][0]),
            nn.ConvTranspose2d(**params_kwargs["output"][1])
        )
                
     
    def forward(self, inputs):
        """
        inputs: EEG data [BxCxTxE]
        
        B: Batch size
        C: channel
        T: Time
        E: Electrode
        """
        out = self.en_module(inputs)
        out = self.de_module(out)
        return out















