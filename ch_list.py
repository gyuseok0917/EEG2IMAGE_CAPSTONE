import mne
import pandas as pd


if __name__ == "__main__":
    # EEG 10-05 System Montage Load
    montage = mne.channels.make_standard_montage("standard_1005")
    ch_name_list = montage.ch_names # channel name list; len = 345
    
    ch_list = []
    for ch_name in ch_name_list:
        answer  = input(f"Do you need {ch_name} channel? (y or n)")
        
        # If required, add to "ch_list"
        if answer == "y":
            ch_list.append(ch_name)
        elif answer == "n":
            pass
    
    file_path = input("Please enter the file root => ")
    df = pd.DataFrame({"ch_name": ch_list})
    df.to_csv(file_path, index = False)