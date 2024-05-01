import torch


def signal_to_noise_ratio(sr_eeg, hr_eeg):
    """
    Function to calculate the SNR (Signal-to-Noise Ratio)
    
    Args:
        sr_eeg: SR (Super Resolution) EEG
        hr_eeg: HR (High Resolution) EEG
    """
    
    # SR EEG signal power
    signal_power = sr_eeg.pow(2).sum()
    
    # Noise Power => (SR - HR)^2's SUM
    noise_power = (sr_eeg - hr_eeg).pow(2).sum()
    
    # SNR Score
    snr = 10 * torch.log10(signal_power / noise_power)
    
    return snr

def pearson_correlation_coefficient(sr_eeg, hr_eeg):
    """
    Function to calculate the PCC (Pearson Correlation Coefficient)
    
    Args:
        sr_eeg: SR (Super Resolution) EEG
        hr_eeg: HR (High Resolution) EEG
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

