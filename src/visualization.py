import mne
import numpy as np
import matplotlib.pyplot as plt

from mne.time_frequency import tfr_array_morlet


def plot_single_channel(
    lr_eeg = None,
    sr_eeg = None,
    hr_eeg = None,
    time_len = None,
    sfreq = None,
    ch_name = None,
    save_path = None
):  
    plt.figure(figsize = (14, 4))
    if lr_eeg is not None: plt.plot(lr_eeg, color = "g", linestyle = "--", label = "LR")
    if sr_eeg is not None: plt.plot(sr_eeg, color = "b", linestyle = "--", label = "SR")
    if hr_eeg is not None: plt.plot(hr_eeg, color = "r", label = "HR")
    plt.title(ch_name, fontsize = 18)
    plt.xlabel("Time [s]", fontsize = 14)
    plt.xticks(np.linspace(0, time_len, 10), np.linspace(0, time_len / sfreq, 10).round(2))
    plt.ylabel(r"Amplitude [$\mu$V]", fontsize = 14)
    plt.grid()
    plt.legend()
    
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()
    plt.close()
    
    
def plot_topomap(raw_eeg, figsize, save_path = None, *args, **kwargs):
    """
    Args:
        raw_eeg (Dict)
            {
                "LR": (EvokedArray) ...,
                "SR": (EvokedArray) ...,
                "HR": (EvokedArray) ...
            }
    """
    fig, axes = plt.subplots(nrows = 1, ncols = len(raw_eeg.keys()), figsize = figsize)
    
    for ax, (title, eeg_data) in zip(axes.flat, raw_eeg.items()):
        topo_data = np.mean(eeg_data.data, axis = 1)
        topo_data = (topo_data - topo_data.mean()) / topo_data.std()
        
        im, cn = mne.viz.plot_topomap(
            topo_data, eeg_data.info, show = False, cmap = 'coolwarm',
            sensors = False, res = 1000, axes=ax, size = 2, vlim = (-1, 1)
        )
 
        ax.set_title(f"{title}")
    cax = fig.add_axes([0.92, 0.33, 0.005, 0.4])
    fig.colorbar(im, cax=cax)
    
    if save_path is not None:
        fig.savefig(save_path)
    
    
def get_morlet(raw_eeg, freqs):
    raw_array = raw_eeg.get_data()
    sfreq = raw_eeg.info['sfreq']
    n_cycles = freqs / 4.

    power = tfr_array_morlet(
        raw_array[np.newaxis],
        sfreq=sfreq,
        freqs=freqs,
        n_cycles=n_cycles,
        output='power'
    )[0, 0]

    return power, sfreq

def show_morlet(raw_eeg, freqs, cmap='viridis', figsize=(10, 6), save_path=None):  
    num_eeg = len(raw_eeg.keys())
    fig, axes = plt.subplots(num_eeg, 1, figsize=(figsize[0], figsize[1] * num_eeg), sharex=True)

    if num_eeg == 1:
        axes = [axes]
        
    all_power = []
    for _, eeg in raw_eeg.items():
        power, sfreq = get_morlet(eeg, freqs)
        all_power.append(power)
        
    vmin = min([p.min() for p in all_power])
    vmax = max([p.max() for p in all_power])

    for i, (title, eeg) in enumerate(raw_eeg.items()):
        ch_name = eeg.info['ch_names'][0]
        power = all_power[i]

        ax = axes[i]
        im = ax.imshow(power, cmap=cmap, aspect='auto', origin='lower',
                       extent=[0, power.shape[-1] / sfreq, freqs[0], freqs[-1]], vmin = vmin, vmax = vmax)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Frequency [Hz]')
        ax.set_title(f'{ch_name} of {title}')
    fig.colorbar(im, ax=axes, label='Power', orientation='vertical', shrink = 0.6)
    
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()
    
    
    
    
    
    
    
    
    