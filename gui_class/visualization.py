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
    
    # 축 범위 지정
    widget.setRange(xRange = (0, 500), disableAutoRange=True)

    # Label 지정
    widget.setLabel("left", "Amplitude")
    widget.setLabel("bottom", "Time [s]")

    # 눈금 수정
    channel_names = [f'Channel {i+1}' for i in range(num_ch)]
    widget.getAxis('left').setTicks([[(i * 3, name) for i, name in enumerate(channel_names)]])
    widget.getAxis('bottom').setTicks([[(idx, f"{round(value, 2)}") for idx, value in zip(np.linspace(0, 500, 10), np.linspace(0, 1, 10))]])

    widget.showGrid(x = True, y = True)