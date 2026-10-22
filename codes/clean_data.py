
# The clean_data.py is used to clean the data of the 
# Impostor Syndrome study dataset.

#This code is made of the following sections:
    # 1. Settings  
    # 2. Remove subjects with NaN  
    # 3. Keep the subjects with IFFS =/= 0 
    # 4. Remove subjects with mean_fd > 0.5 mm
    # 5. Threshold FC matrix
    # 6. Save the new dataset

#--------------
# 1. Settings 
#--------------

#import all the necessary packages 

from pathlib import Path

import numpy as np
import pandas as pd

# load your data 

# -- participants csv --
#participants = pd.read_csv("../data/participants.csv")
PROJECT_DIR = Path.cwd()  # only if the working directory is the project root
DATA_DIR = PROJECT_DIR / "data" # i save the generated dataset in the data folder

participants_cvs = DATA_DIR / "participants.csv"
participants = pd.read_csv(participants_cvs)

# -- connectivity matrix --
fc_file = DATA_DIR / "connectivity_matrices.npz"
fc_data = np.load(fc_file)

print(fc_data.files) #know your key to store the data 

fc_matrices = fc_data["matrices"]

roi_names = [
    "mPFC", "PCC", "L_Angular", "R_Angular",
    "L_Insula", "dACC", "L_dlPFC", "R_dlPFC"
]

# ------------------------------------
# 2. Remove subjects with NaN
# ------------------------------------ 
participants_clean = participants.loc[~participants.isna().any(axis=1)]

print(f"Remaining subjects: {len(participants_clean)}")

# ------------------------------------
# 3. Keep the subjects with IFFS =/= 0
# ------------------------------------ 
print(f"Participants with IFFS=0: {(participants_clean["ifss_score"] == 0).sum()}")

participants_clean = participants_clean.loc[participants_clean["ifss_score"] != 0].copy()

# check that the participants that remain match the data quality report
print(f"Remaining subjects: {len(participants_clean)}")

# check that you actually deleted all the subject with IFSS=0
print(f"Subjects with IFSS = 0: {(participants_clean['ifss_score'] == 0).sum()}")

# -----------------------------------------
# 4. Remove subjects with mean_fd > 0.5 mm
# ----------------------------------------- 
print(f"Participants with mean_fd > 0.5 mm: {(participants_clean["mean_fd"] > 0.5).sum()}")

participants_clean = participants_clean.loc[participants_clean["mean_fd"] < 0.50].copy()

# check that the participants that remain match the data quality report
print(f"Remaining subjects: {len(participants_clean)}")

# check that you actually deleted all the subject with IFSS=0
print(f"Subjects with mean_fd > 0.5: {(participants_clean["mean_fd"] > 0.50).sum()}")

# -----------------------
# 5. Threshold FC matrix
# -----------------------

# choose the FC threshold
threshold = 0.05

# create a copy of the original matrices
fc_thresholded = fc_matrices.copy()

# remove weak connections
fc_thresholded[np.abs(fc_thresholded) <= threshold] = 0

# keep the diagonal equal to 1 for every participant
idx = np.arange(fc_thresholded.shape[1])
fc_thresholded[:, idx, idx] = 1

# select the FC matrices of the subjects that were not discarded before 
 
# map subject IDs to their original matrix positions
subject_to_index = {
    subject_id: i
    for i, subject_id in enumerate(participants["subject_id"])
}

# get positions of the retained participants
indices = [
    subject_to_index[sid]
    for sid in participants_clean["subject_id"]
]

# retrieve the corresponding FC matrices
fc_clean = fc_matrices[indices].copy()

# -----------------------
# 6. Save the database
# -----------------------

# save a new participant table 
participants_clean.to_csv(
    DATA_DIR / "participants_clean.csv",
    index=False,
)

# save the new connectivity matrices 
np.savez_compressed(
    DATA_DIR / "connectivity_matrices_clean.npz",
    matrices=fc_clean,
    subject_ids= participants_clean.subject_id,
    roi_names=np.array(roi_names),
)