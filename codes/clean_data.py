
# The clean_data.py is used to clean the data from the 
# Impostor Syndrome dataset.

#This code is made of the following sections:
    # 1. Settings  
    # 2. Remove subjects with NaN values 
    # 3. Keep the subjects with IFFS =/= 0 
    # 4. Remove subjects with mean_fd > 0.5 mm
    # 5. Threshold FC matrix

# 1. Settings 
#import all the necessary packages 

from IPython.display import display
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# load your data 

# -- participants csv --
participants = pd.read_csv("../data/participants.csv")
#participants = pd.read_csv("data/participants.csv")

# -- connectivity matrix --
fc_file = Path("../data/connectivity_matrices.npz")
fc_data = np.load(fc_file)

print(fc_data.files) #know your key to store the data 

fc_matrices = fc_data["matrices"]

roi_names = [
    "mPFC", "PCC", "L_Angular", "R_Angular",
    "L_Insula", "dACC", "L_dlPFC", "R_dlPFC"
]

# ------------------------------------
# 2. Remove subjects that are NaN
# ------------------------------------ 
participants = participants.loc[~participants.isna().any(axis=1)]

print(f"Remaining subjects: {len(participants)}")

# ------------------------------------
# 3. Keep the subjects with IFFS =/= 0
# ------------------------------------ 
print(f"Participants with IFFS=0: {(participants["ifss_score"] == 0).sum()}")

participants = participants.loc[participants["ifss_score"] != 0].copy()

# check that the participants that remain match the data quality report
print(f"Remaining subjects: {len(participants)}")

# check that you actually deleted all the subject with IFSS=0
print(f"Subjects with IFSS = 0: {(participants['ifss_score'] == 0).sum()}")

# -----------------------------------------
# 4. Remove subjects with mean_fd > 0.5 mm
# ----------------------------------------- 
print(f"Participants with mean_fd > 0.5 mm: {(participants["mean_fd"] > 0.5).sum()}")

participants = participants.loc[participants["mean_fd"] < 0.50].copy()

# check that the participants that remain match the data quality report
print(f"Remaining subjects: {len(participants)}")

# check that you actually deleted all the subject with IFSS=0
print(f"Subjects with mean_fd > 0.5: {(participants["mean_fd"] > 0.50).sum()}")

# -----------------------
# 5. Threshold FC matrix
# -----------------------

