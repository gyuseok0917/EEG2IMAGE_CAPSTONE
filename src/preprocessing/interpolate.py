import numpy as np

from scipy.interpolate import Rbf


def rbf_interpolation(eeg_data, selected_positions, all_positions, interp_fn, *args, **kwargs):
    """
    Provides the ability to interpolate EEG signals using Radial Basis Function.
    
    Based on the input data and channel location information,
    channels are interpolated considering spatial characteristics.
    
    Args:
        eeg_data: Input EEG signal [Electrode, Time]
        selected_positions: Channel location information of input data
        all_positions: Location information for all channels
        interp_fn: Select interpolation method
        
        1) 'multiquadric': sqrt((r/self.epsilon)**2 + 1)
        2) 'inverse': 1.0/sqrt((r/self.epsilon)**2 + 1)
        3) 'gaussian': exp(-(r/self.epsilon)**2)
        4) 'linear': r
        5) 'cubic': r**3
        6) 'quintic': r**5
        7) 'thin_plate': r**2 * log(r)
    """
    
    # Time-axis size
    T = eeg_data.shape[-1]
    
    # [N_total channels, T]
    interpolated_data = np.zeros((len(all_positions), T))
    
    # Interpolate for each time point
    for t_idx in range(T):
        sample = eeg_data[:, t_idx]
        
        rbf = Rbf(
            selected_positions[:, 0],
            selected_positions[:, 1],
            selected_positions[:, 2],
            sample,
            function = interp_fn,
            *args,
            **kwargs
        )
        
        interpolated_data[:, t_idx] = rbf(
            all_positions[:, 0],
            all_positions[:, 1],
            all_positions[:, 2]
        )
    
    return interpolated_data




