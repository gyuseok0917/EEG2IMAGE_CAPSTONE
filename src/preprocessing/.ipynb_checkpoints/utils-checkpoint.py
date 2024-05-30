import torch
import numpy as np


def z_score_standardization(data):
    return (data - data.mean()) / data.std()


def robust_scaling(data):
    median = data.median(axis = 0).values
    q75, q25 = data.quantile(0.75, dim = 0), data.quantile(0.25, dim = 0)
    iqr = q75 - q25
    
    return (data - median) / (iqr + 1e-9) # (data - median) / (iqr + 1e-9)


def custom_norm(data):
    norm = data.max() / 2.0
    
    return (data - norm) / norm