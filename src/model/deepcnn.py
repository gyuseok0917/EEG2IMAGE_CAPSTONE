import torch
import torch.nn as nn
import torch.nn.functional as F


class DeepCNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Encoder process
        self.conv1 = nn.Conv2d(1, 64, kernel_size = (13, 5), stride = 2, padding = 1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size = (13, 5), stride = 2, padding = 1)
        self.conv3 = nn.Conv2d(64, 64, kernel_size = (13, 5), stride = 2, padding = 1)
        
        # Decoder process
        self.deconv1 = nn.ConvTranspose2d(64, 64, kernel_size = (13, 9), stride = 2, padding = 1, output_padding = 1)
        self.deconv2 = nn.ConvTranspose2d(64, 64, kernel_size = (13, 9), stride = 2, padding = 1, output_padding = 1)
        self.deconv3 = nn.ConvTranspose2d(64, 64, kernel_size = (13, 9), stride = 2, padding = 1, output_padding = 1)

        self.conv4 = nn.Conv2d(64, 64, kernel_size = (13, 5), stride = 1, padding = 1)
        self.conv5 = nn.Conv2d(64, 1, kernel_size = (7, 1), stride = 1, padding = 1)

    
    def forward(self, inputs):
        out = F.prelu(self.conv1(inputs))
        out = F.prelu(self.conv2(out))
        out = F.prelu(self.conv3(out))
        
        out = F.prelu(self.deconv1(out))
        out = F.prelu(self.deconv2(out))
        out = F.prelu(self.deconv3(out))
        out = F.prelu(self.conv4(out))
        out = F.prelu(self.conv5(out))
        return out
