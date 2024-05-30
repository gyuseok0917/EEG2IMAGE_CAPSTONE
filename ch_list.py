import os
os.chdir("/workspace")
import mne
import pandas as pd


DIR = "data/EEG_ImageNet"

if __name__ == "__main__":
    montage = mne.channels.make_standard_montage("standard_1005")
    ch_name_list = montage.ch_names
    
    ch_list = []
    for ch_name in ch_name_list:
        answer  = input(f"Do you need {ch_name} channel? (y or n)")
        
        if answer == "y":
            ch_list.append(ch_name)
        elif answer == "n":
            pass
    
    file_name = input("Please enter the file name => ")
    df = pd.DataFrame({"ch_name": ch_list})
    df.to_csv(os.path.join(DIR, file_name), index = False)
















