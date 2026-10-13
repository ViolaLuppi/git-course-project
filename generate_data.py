# This code is used to produce the synthetic data that are going to be used 
# in the project for the course: 'Open Science in Practice: Collaborative Research in Git. 
# This code generates: N functional connectivity (FC) for N subjects, demographics, clinical scales. 
# All data generated in this code is fictitious. 
# The clinical scales used for the sole objective of generatig covairates
# to simulate a clinical study and should not be used for clinical purposes. 

# The code contains the following sections: 
    # 1. Settings 
    # 2. Define the ROIs 

# 1. Settings: install all the required packages and generate the folder 
# where you are going to keep your raw data. 

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_SUBJECTS = 120 #the number of subjects in this dataset
N_ROIS = 8 #the number of ROIs that we are going to consider for FC
N_TIMEPOINTS = 180 

OUTPUT_DIR = Path(r"data") # insert your path 
OUTPUT_DIR.mkdir(exist_ok=True) # if the folder does not already exist, a new folder will be added to the specified path

rng = np.random.default_rng(SEED) #always generate the same sequence of pseudo-random numbers 

# 2. Define the ROIs
# These are chosen randomly but are existing ROIs. 

roi_names = [
    "mPFC",
    "PCC",
    "L_Angular",
    "R_Angular",
    "L_Insula",
    "dACC",
    "L_dlPFC",
    "R_dlPFC",
]

# 3. Generate participants information
# Include IDs, age, sex, Impostor Feeling Syndrome Score (IFSS) and Anxiety Score (AS).  

# The IDs will look like 001, 002, 003 since we have more than 99 subjects. 
subject_ids = [
    f"sub-{i:03d}" for i in range(1, N_SUBJECTS + 1)
]

# Age range will be 18 - 45
age = rng.integers(18, 46, size=N_SUBJECTS)

# Each participant is randomly assigned their sex. 
# p defines the probability of being assigned F (0.7) or M (0.3)
sex = rng.choice(
    ["F", "M"],
    size=N_SUBJECTS,
    p=[0.7, 0.3],
)

# IFSS: random numbers from a normal distribution with mean 60 and standard deviation 13. 
# The range is between 20-100. Then round the values and convert them to integers

ifss = np.clip(
    rng.normal(60, 13, size=N_SUBJECTS),
    20,
    100,
).round().astype(int)


# AS is made relatively associated to the IFs score. 
anxiety = (
    20
    + 0.25 * (ifss - 60)
    + rng.normal(0, 6, size=N_SUBJECTS)
)

# It is kept between 0 and 40
anxiety = np.clip(anxiety, 0, 40).round().astype(int)

# Our covariates become an actual data frame 
participants = pd.DataFrame({
    "subject_id": subject_ids,
    "age": age,
    "sex": sex,
    "ifss_score": ifss,
    "anxiety_score": anxiety,
})

# 4. Define the connectivity structure
# In this part of the code we define the connectivity matrix. 
# The idea behind it is that we are going to generate stronger correlations between the ROIs that belong to specific networks:
#  - Default Mode Network (DMN)
#  - Saliene Network (SN)
#  - Executive Control Network (ECN)

# generate the 8 x 8 matrix 
base_corr = np.full((N_ROIS, N_ROIS), 0.05)


# we choose mPFC, PCC, L_Angular and R_Angular which are part of the (DMN)
# and assign them stronger correlations. 
dmn_rois = [0, 1, 2, 3]

for i in dmn_rois:
    for j in dmn_rois:
        if i != j:
            base_corr[i, j] = 0.25

# We do the same for the ROIs (L_Insula, dACC) of SN and the ROIs (L_dlPFC, R_dlPFC) of ECN.  
base_corr[4, 5] = 0.25
base_corr[5, 4] = 0.25

base_corr[6, 7] = 0.25
base_corr[7, 6] = 0.25

# The matrix has 1 on its diagonal (each ROI has the highest correlation with itself)
np.fill_diagonal(base_corr, 1.0)


# 5. Generate one FC matrix per participant

fc_matrices = []

for score in ifss:

    # I generate mildly weaker connectivity within the DMN associated to higher IFSS. 

    score_effect = (score - 60) / 40 * 0.08

    subject_corr = base_corr.copy()

    for i in dmn_rois:
        for j in dmn_rois:
            if i != j: # only when i get two different ROIs 
                subject_corr[i, j] -= score_effect # i subtract the score effect to the base correlation

    # generate some time series for each ROI
    roi_signals = rng.multivariate_normal(
        mean=np.zeros(N_ROIS), # I set the mean of the signal to 0
        cov=subject_corr, # the time series respects the correlation structure I want for my FC. 
        size=N_TIMEPOINTS, # the signal is made of 180 data samples (rows of the matrix)
    )

    # calculate the functional connectivity matrix.
    fc = np.corrcoef(roi_signals, rowvar=False)

    fc_matrices.append(fc)


fc_matrices = np.array(fc_matrices)



# 6. Save the synthetic database

participants.to_csv(
    OUTPUT_DIR / "participants.csv",
    index=False,
)

np.savez_compressed(
    OUTPUT_DIR / "connectivity_matrices.npz",
    matrices=fc_matrices,
    subject_ids=np.array(subject_ids),
    roi_names=np.array(roi_names),
)

print("Synthetic database generated successfully!")

print(f"Number of participants: {len(participants)}")
print(f"Connectivity matrices shape: {fc_matrices.shape}")
print(f"Participant table shape: {participants.shape}")
print(f"Files saved in: {OUTPUT_DIR.resolve()}")
