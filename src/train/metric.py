import torch


def signal_to_noise_ratio(sr_eeg, hr_eeg):
    """
    Function to calculate the SNR (Signal-to-Noise Ratio)
    
    Args:
        sr_eeg: SR (Super Resolution) EEG [BxCxTxE]
        hr_eeg: HR (High Resolution) EEG  [BxCxTxE]
    """
    
    eps = torch.finfo(sr_eeg.dtype).eps
    
    signal_power = hr_eeg.pow(2).sum()
    noise_power = (hr_eeg - sr_eeg).pow(2).sum()
    
    snr_value = (signal_power + eps) / (noise_power + eps)
    
    return 10 * torch.log10(snr_value) 
    

def pearson_correlation_coefficient(sr_eeg, hr_eeg):
    """
    Function to calculate the PCC (Pearson Correlation Coefficient)
    
    Args:
        sr_eeg: SR (Super Resolution) EEG [BxCxTxE]
        hr_eeg: HR (High Resolution) EEG  [BxCxTxE]
    """
    
    # Calculate Deviation
    sr_deviation = sr_eeg - sr_eeg.mean()
    hr_deviation = hr_eeg - hr_eeg.mean()
    
    # Calculate PCC
    numerator = (sr_deviation * hr_deviation).sum()
    denominator = torch.sqrt(sr_deviation.pow(2).sum() * hr_deviation.pow(2).sum())
    
    if denominator == 0:
        return 0  # 분모가 0인 경우 예외 처리
    
    return numerator / denominator

