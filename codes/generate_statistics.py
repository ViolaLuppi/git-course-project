# In this code we generate two Generalized Linear Models (GLM) 
# for the FC analysis in the Impostor Syndrome database.
# Both models test the association between IFSS and connectivity. 
# However, the first model is adjusted for age, sex and mean head motion, 
# while the second is also adjusted for anxiety scale. 

from pathlib import Path

import numpy as np
import pandas as pd
# pyrefly: ignore[missing-import]
import statsmodels.formula.api as smf
from IPython.display import display
# pyrefly: ignore[missing-import]
from statsmodels.stats.multitest import multipletests

PROJECT_DIR = Path.cwd()  # only if the working directory is the project root
DATA_DIR = PROJECT_DIR / "data" # i save the generated dataset in the data folder

participants_cvs = DATA_DIR / "participants_clean.csv"
participants_clean = pd.read_csv(participants_cvs)

# -- connectivity matrix --
fc_file = DATA_DIR / "connectivity_matrices_clean.npz"
fc_data = np.load(fc_file)

fc_matrices_clean = fc_data["matrices"]

roi_names = [
    "mPFC", "PCC", "L_Angular", "R_Angular",
    "L_Insula", "dACC", "L_dlPFC", "R_dlPFC"
]

# prepare the covariate table. 
# We already include anxiety score, but we will use it only for model 2

required_columns = [
    "ifss_score", "anxiety_score", "age", "sex", "mean_fd"
]

# this is a mask we use to make sure we don't have any missing value
complete_mask = participants_clean[required_columns].notna().all(axis=1)

# this applies the mask to retain only participants with complete data.
participants_analysis = (
    participants_clean.loc[complete_mask].copy().reset_index(drop=True)
)

# select the corresponding FC matrices for each participant 
fc_analysis = fc_matrices_clean[complete_mask.to_numpy()].copy()

# check that the participants number and matrix size correspond 
print("Participants included in both models:", len(participants_analysis))
print("FC matrices:", fc_analysis.shape)

# extract each unique ROI-to-ROI connection
upper_idx = np.triu_indices(len(roi_names), k=1)

results = []

for i, j in zip(*upper_idx):

    # one row per participant, with the FC value as the outcome
    df = participants_analysis.copy()
    df["FC"] = fc_analysis[:, i, j]

    # Model 1: IFSS + age + sex + mean FD
    model1 = smf.ols(
        "FC ~ ifss_score + age + C(sex) + mean_fd",
        data=df
    ).fit()

    # Model 2: IFSS + anxiety + age + sex + mean FD
    model2 = smf.ols(
        "FC ~ ifss_score + anxiety_score + age + C(sex) + mean_fd",
        data=df
    ).fit()

    results.append({
        "ROI_1": roi_names[i],
        "ROI_2": roi_names[j],
        "beta_IFSS_model1": model1.params["ifss_score"],
        "p_IFSS_model1": model1.pvalues["ifss_score"],
        "beta_IFSS_model2": model2.params["ifss_score"],
        "p_IFSS_model2": model2.pvalues["ifss_score"],
        "N": int(model1.nobs)
    })

results_df = pd.DataFrame(results)

# correct the 28 IFSS tests separately for each model
results_df["p_FDR_model1"] = multipletests(
    results_df["p_IFSS_model1"], method="fdr_bh"
)[1]

results_df["p_FDR_model2"] = multipletests(
    results_df["p_IFSS_model2"], method="fdr_bh"
)[1]

# sort by the adjusted p-value from Model 2
results_df = results_df.sort_values("p_FDR_model2")

# display the table
display(results_df.round(4))

# save the results
results_df.to_csv(
    PROJECT_DIR / "results/fc_glm_results.csv",
    index=False
)