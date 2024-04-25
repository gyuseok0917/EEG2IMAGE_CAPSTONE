import numpy as np

def add_white_gaussian_noise(eeg_signal, snr_ratio):
    """
    White Gaussian Noise Add Function
    
    Args:
        eeg_signal (np.ndarray): EEG data (CxT) # C: electrode T: Measurement time
        snr_ratio (float): Signal-to-Noise Ratio
    Return (np.ndarray):
        EEG data with added noise
    """
    eeg_power = np.mean(np.square(eeg_signal))
    
    noise_power = eeg_power / (10 ** (snr_ratio / 10))
    WGN = np.random.normal(scale = np.sqrt(noise_power), size = eeg_signal.shape)
    noisy_eeg_signal = eeg_signal + WGN
    return noisy_eeg_signal


def add_real_noise(eeg_signal, real_noise_data, snr_ratio):
    """
    Real Noise Add Function
    
    Args:
        eeg_signal (np.ndarray): EEG data (CxT) # C: electrode T: Measurement time
        real_noise_data (np.ndarray): A matrix of the same size as "eeg_signal" of real noise.
        snr_ratio (float): Signal-to-Noise Ratio
    Return (np.ndarray):
        EEG data with added noise
    """
    eeg_power = np.mean(np.square(eeg_signal))
    noise_power = np.mean(np.square(real_noise_data))
    
    target_noise_power = eeg_power / (10 ** (snr_ratio / 10))
    scale_factor = np.sqrt(target_noise_power / noise_power)
    scaled_noise_data = real_noise_data * scale_factor
    
    noisy_eeg_signal = eeg_signal + scaled_noise_data
    
    return noisy_eeg_signal