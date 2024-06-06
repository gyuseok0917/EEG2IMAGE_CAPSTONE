import mne
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt

from mne import Info
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import pyqtSignal, QObject


class EEGPlotter(QObject):
    regionChanged = pyqtSignal(float, float)  # 신호 정의: 두 개의 float 값 및 EEG Info를 전달

    def __init__(self, widget, generate_sr_eeg, ground_truth_eeg = None):
        super().__init__()
        self.widget = widget
        self.generate_sr_eeg = generate_sr_eeg
        self.ground_truth_eeg = ground_truth_eeg
        self.region = pg.LinearRegionItem()
        self.init_plot()

    def init_plot(self):
        channel_names = self.generate_sr_eeg.info["ch_names"]
        sfreq = self.generate_sr_eeg.info["sfreq"]

        num_ch, self.num_samples = self.generate_sr_eeg.get_data().shape
        time = self.num_samples / sfreq
        spacing = 3

        for ch_idx in range(num_ch):
            # 생성된 (Ground Truth) EEG 시각화 코드
            generate_sample = self.generate_sr_eeg.get_data()[ch_idx]
            generate_sample_minmax = (generate_sample - generate_sample.mean()) / generate_sample.std()
            self.widget.plot(np.arange(self.num_samples), generate_sample_minmax + ch_idx * spacing, pen=pg.mkPen('b'))

            # 정답(Ground Truth) EEG 시각화 코드
            if self.ground_truth_eeg is not None:
                gt_sample = self.ground_truth_eeg.get_data()[ch_idx]
                gt_sample_minmax = (gt_sample - gt_sample.mean()) / gt_sample.std()
                self.widget.plot(np.arange(self.num_samples), gt_sample_minmax + ch_idx * spacing, pen=pg.mkPen('b'))

        self.widget.setLabel("left", "Amplitude")
        self.widget.setLabel("bottom", "Time [s]")
        self.widget.getAxis('left').setTicks([[(i * spacing, name) for i, name in enumerate(channel_names)]])
        self.widget.getAxis('bottom').setTicks([[(idx, f"{round(value, 2)}") for idx, value in
                                                 zip(np.linspace(0, self.num_samples, 10), np.linspace(0, time, 10))]])
        self.widget.getViewBox().setYRange(0, spacing * 8)
        self.widget.getViewBox().setXRange(0, self.num_samples)
        self.widget.showGrid(x=True, y=True)

        self.region.setRegion([0, 0])
        self.widget.addItem(self.region, ignoreBounds=True)
        self.region.sigRegionChanged.connect(self.ON_REGION_CHANGED)

    def ON_REGION_CHANGED(self):
        t_min, t_max = self.region.getRegion()

        if t_min < 0:
            t_min = 0
        if t_max > self.num_samples:
            t_max = self.num_samples
        self.regionChanged.emit(t_min, t_max)


def TOPOMAP(raw_eeg, tmin, tmax):
    print(tmin, tmax)

    if round(tmin) == round(tmax):
        topo_data = raw_eeg.get_data()[:, round(tmin)]
    else:
        topo_data = raw_eeg.get_data()[:, round(tmin):round(tmax)]
        topo_data = np.mean(topo_data, axis=1)
    topo_data = (topo_data - np.mean(topo_data)) / np.std(topo_data)

    fig, ax = plt.subplots()
    im, _ = mne.viz.plot_topomap(
        topo_data, raw_eeg.info, show=False, cmap='coolwarm',
        sensors=False, res=1000, axes=ax, size=2, vlim=(-1, 1)
    )
    ax.set_title('%.2f-%.2f [s]' % (tmin / raw_eeg.info["sfreq"], tmax / raw_eeg.info["sfreq"]))
    fig.colorbar(im)

    fig.canvas.draw()
    buf = fig.canvas.tostring_rgb()
    w, h = fig.canvas.get_width_height()
    image = QImage(buf, w, h, QImage.Format.Format_RGB888)
    image = QPixmap.fromImage(image)

    return image
