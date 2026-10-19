
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

# To isolate significant connections we threshold the FC matrices. 
# First we see the effect of applying different thresholds and then
# we apply the threshold. 

# LOADING THE CONNECTIVITY MATRIX
fc_file = np.load("data/connectivity_matrices.npz")

#make sure of the key you used to save the connectivity matrix
print(fc_file.files) 

# in my case it is 'matrices'
fc_matrices = fc_file["matrices"]

# Define some thresholds to see 
thresholds = np.arange(0.05, 0.45, 0.05)

mean_connections = []
mean_density = []

#because connectivity matrices are symmetric, 
# we get each connection once by considering the upper triangle in the matrix
upper_idx = np.triu_indices(len(roi_names), k=1)

n_possible = len(roi_names) * (len(roi_names) - 1) // 2

for threshold in thresholds:
    # Keep connections with |r| greater than the threshold
    retained = np.abs(
        fc_matrices[:, upper_idx[0], upper_idx[1]]
    ) > threshold

    mean_connections.append(retained.sum(axis=1).mean())
    mean_density.append(retained.mean())

# plot the remaining connection on average depending on the threshold 
plt.figure(figsize=(8, 5))
plt.plot(thresholds, mean_density, marker="o")
plt.xlabel("Absolute FC threshold")
plt.ylabel("Mean network density")
plt.title("Effect of Threshold on FC Network Density")
plt.ylim(0, 1)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# print the value 
for threshold, n_conn, density in zip(
    thresholds, mean_connections, mean_density
):
    print(
        f"Threshold = {threshold:.2f} | "
        f"Mean connections = {n_conn:.1f}/{n_possible} | "
        f"Density = {density:.1%}"
    )

# Choose the FC threshold
threshold = 0.05

# Create a copy of the original matrices
fc_thresholded = fc_matrices.copy()

# Remove weak connections
fc_thresholded[np.abs(fc_thresholded) <= threshold] = 0

# Keep the diagonal equal to 1 for every participant
idx = np.arange(fc_thresholded.shape[1])
fc_thresholded[:, idx, idx] = 1