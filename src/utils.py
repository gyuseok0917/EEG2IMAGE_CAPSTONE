import os
import json
import pickle
import oyaml as yaml
import pandas as pd


def exist_path(path):
    return os.path.exists(path)


def read_config(path):
    formats = path.split('.')[-1]
    
    if formats == "json":
        with open(path, "r") as F:
            config = json.load(F)
    elif formats == "pkl":
        with open(path, "rb") as F:
            config = pickle.load(F)
    elif formats == "yml":
        with open(path) as F:
            config = yaml.load(F, Loader = yaml.FullLoader)
    return config


def save_log(logs: dict, save_path):
    
    log_df = pd.DataFrame(logs)
    
    if exist_path(save_path):
        log_df.to_csv(save_path, mode = "a", header = False, index = False)
    else:
        log_df.to_csv(save_path, index = False)


        
        
        
        
        
        
        
        
        
        