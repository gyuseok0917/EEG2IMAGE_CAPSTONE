from scipy.signal import butter, filtfilt


class ButterworthFilter:
    """
    This is a custom class that provides functionality for applying Butterworth filters.
    
    Args:
        l_freq (int or float): Frequency value to low pass
        h_freq (int or float): Frequency value to high pass
        fs (int or float): Sampling rate of input data
        order (int): Order of filter
    """
    def __init__(self, l_freq, h_freq, fs, order = 2):
        
        assert l_freq is not None and h_freq is not None, "Both l_freq and h_freq cannot have the value None."
        
        nyq = 0.5 * fs # Nyquist Frequency
        
        if l_freq is None:
            self.Wn = [h_freq / nyq]
        elif h_freq is None:
            self.Wn = [l_freq / nyq]
        else:
            self.Wn = [l_freq / nyq, h_freq / nyq]
        
        self.order = order
        
    
    def bandpass(self, btype, output = "sos", *args, **kwargs):
        """
        Parameters:                
            btype: Filter type (lowpass, highpass, bandpass, bandcut)
        """
        b, a = butter(self.order, self.Wn, btype = btype, output = output, *args, **kwargs)
        return b, a
    
    
    def butterworth_filter(self, channel_per_eeg, *args, **kwargs):
        """
        Parameters:
            channel_per_eeg: EEG Single channel data
        """
        b, a = self.bandpass(*args, **kwargs)
        y = filtfilt(b, a, channel_per_eeg)
        return y
    
    
    def __call__(self, eeg_signal, *args, **kwargs):
        """
        Parameters:
            eeg_signal: EEG data [Electrode, Time]
        """
            
        filtered_singal = np.array([
            self.butterworth_filter(channel_per_eeg, *args, **kwargs)
            for channel_per_eeg in eeg_signal
        ])
        
        return filtered_singal



