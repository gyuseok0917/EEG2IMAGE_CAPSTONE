📦EEGStyleGAN-ADA
 ┣ 📂anaconda
 ┃ ┗ 📜to1.7.yml
 ┣ 📂dataset
 ┃ ┣ 📂eeg_imagenet40_cvpr_2017_raw
 ┣ ┃ ┣ 📂test
 ┃ ┃ ┃ ┗ 📜.npy
 ┃ ┃ ┣ 📂train
 ┃ ┃ ┃ ┗ 📜.npy
 ┃ ┃ ┣ 📂val
 ┃ ┃ ┃ ┗ 📜.npy
 ┃ ┣ 📂new_sr
 ┣ ┃ ┣ 📂test
 ┃ ┃ ┃ ┗ 📜.npy
 ┃ ┃ ┣ 📂train
 ┃ ┃ ┃ ┗ 📜.npy
 ┃ ┃ ┣ 📂val
 ┃ ┃ ┃ ┗ 📜.npy
 ┣ 📂EEG2Feat
 ┃ ┗ 📂Triplet_LSTM
 ┃ ┃ ┣ 📂CVPR40
 ┃ ┃ ┃ ┣ 📂EXPERIMENT_29
 ┃ ┃ ┃ ┃ ┣ 📂bestckpt
 ┃ ┃ ┃ ┃ ┃ ┗ 📜eegfeat_all_0.9665178571428571.pth
 ┃ ┃ ┃ ┃ ┗ 📂finetune_bestckpt
 ┃ ┃ ┃ ┃ ┃ ┗ 📜eegfeat_all_0.9833920483140413.pth
 ┃ ┃ ┃ ┣ 📜config.py
 ┃ ┃ ┃ ┣ 📜dataaugmentation.py
 ┃ ┃ ┃ ┣ 📜dataloader.py
 ┃ ┃ ┃ ┣ 📜evaluate.py
 ┃ ┃ ┃ ┣ 📜finetuning.py
 ┃ ┃ ┃ ┣ 📜image3dplot.py
 ┃ ┃ ┃ ┣ 📜linearprobing.py
 ┃ ┃ ┃ ┣ 📜losses.py
 ┃ ┃ ┃ ┣ 📜network.py
 ┃ ┃ ┃ ┣ 📜train.py
 ┃ ┃ ┃ ┣ 📜triplet_semihardloss.py
 ┃ ┃ ┃ ┗ 📜visualizations.py
 ┣ 📂EEGStyleGAN-ADA_CVPR40
 ┃ ┣ 📂dnnlib
 ┃ ┃ ┣ 📜util.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂docs
 ┃ ┃ ┣ 📜dataset-tool-help.txt
 ┃ ┃ ┣ 📜license.html
 ┃ ┃ ┗ 📜train-help.txt
 ┃ ┣ 📂eegbestckpt
 ┃ ┃ ┗ 📜eegfeat_lstm_all_0.9665178571428571.pth
 ┃ ┣ 📂imageckpt
 ┃ ┃ ┗ 📜readme.md
 ┃ ┣ 📂metrics
 ┃ ┃ ┣ 📜frechet_inception_distance.py
 ┃ ┃ ┣ 📜inception_score.py
 ┃ ┃ ┣ 📜kernel_inception_distance.py
 ┃ ┃ ┣ 📜metric_main.py
 ┃ ┃ ┣ 📜metric_utils.py
 ┃ ┃ ┣ 📜perceptual_path_length.py
 ┃ ┃ ┣ 📜precision_recall.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂torch_utils
 ┃ ┃ ┣ 📂ops
 ┃ ┃ ┃ ┣ 📜bias_act.cpp
 ┃ ┃ ┃ ┣ 📜bias_act.cu
 ┃ ┃ ┃ ┣ 📜bias_act.h
 ┃ ┃ ┃ ┣ 📜bias_act.py
 ┃ ┃ ┃ ┣ 📜conv2d_gradfix.py
 ┃ ┃ ┃ ┣ 📜conv2d_resample.py
 ┃ ┃ ┃ ┣ 📜fma.py
 ┃ ┃ ┃ ┣ 📜grid_sample_gradfix.py
 ┃ ┃ ┃ ┣ 📜upfirdn2d.cpp
 ┃ ┃ ┃ ┣ 📜upfirdn2d.cu
 ┃ ┃ ┃ ┣ 📜upfirdn2d.h
 ┃ ┃ ┃ ┣ 📜upfirdn2d.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📜custom_ops.py
 ┃ ┃ ┣ 📜misc.py
 ┃ ┃ ┣ 📜persistence.py
 ┃ ┃ ┣ 📜training_stats.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂training
 ┃ ┃ ┣ 📜augment.py
 ┃ ┃ ┣ 📜dataset.py
 ┃ ┃ ┣ 📜loss.py
 ┃ ┃ ┣ 📜networks.py
 ┃ ┃ ┣ 📜training_loop.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜calc_metrics.py
 ┃ ┣ 📜cmd.txt
 ┃ ┣ 📜cmd_generate.txt
 ┃ ┣ 📜cmd_image2eeg2image.txt
 ┃ ┣ 📜cmd_metricalc.txt
 ┃ ┣ 📜config.py
 ┃ ┣ 📜dataset_tool.py
 ┃ ┣ 📜Dockerfile
 ┃ ┣ 📜docker_run.sh
 ┃ ┣ 📜generate.py
 ┃ ┣ 📜image2eeg2image.py
 ┃ ┣ 📜legacy.py
 ┃ ┣ 📜LICENSE.txt
 ┃ ┣ 📜make_json_label.py
 ┃ ┣ 📜metriccompute.sh
 ┃ ┣ 📜network.py
 ┃ ┣ 📜projector.py
 ┃ ┣ 📜readme.md
 ┃ ┣ 📜style_mixing.py
 ┃ ┣ 📜train.py
 ┃ ┗ 📜visualizations.py
 ┣ 📜LICENSE
 ┗ 📜README.md