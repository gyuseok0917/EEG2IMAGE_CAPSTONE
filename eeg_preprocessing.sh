#!/bin/bash
python eeg_preprocessing.py --data_path="data/eegmmidb/eeg_0_80.npy" --snr_ratio=0 --interpolate="multiquadric" --smooth 0 --save_path="data/eegmmidb/preprocessing/noiseless_std.pth"