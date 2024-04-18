import numpy as np


def eeg_plot(widget, eeg_data):
    """
    EEG 데이터를 시각화하는 함수

    Args:
        widget: 시각화할 widget object
    """

    # 채널 수 및 샘플 길이
    num_ch, num_samples = eeg_data.shape

    # stack line plot 그리기
    for ch_idx in range(num_ch):
        widget.plot(np.arange(num_samples), eeg_data[ch_idx] + ch_idx * 3, pen = "b")
    
    widget.setLabel("left", "Amplitude")
    widget.setLabel("bottom", "Time [s]")
    widget.setXRange(0, 500)
    widget.showGrid(x = True, y = True)

    channel_names = [f'Channel {i+1}' for i in range(num_ch)]
    widget.getAxis('left').setTicks([[(i * 3, name) for i, name in enumerate(channel_names)]])