# git-course-project

This repository contains the project *"Impostor Syndrome study"* produced for the course "Open Science in Practice: Collaborative Research in Git" held in October 2026 at Karolinska Institutet.

## Purpose

The files in this repository were created to:

- Generate a dataset of subjects affected by Impostor Syndrome.

- Perform statistical analysis on the generated datasets.

- Document the process in the detail through reports.

## Resources

### Softwares

Python (3.12.15)

Quarto

#### To run the code

You can run the code from the console using:

- `import code.py` **if you run it for the first time**
- `exec(open("path to your code").read())` **from the second time**

### Python packages

`pandas` - Used for dataframes.

`numpy` - Used for working with arrays.

`matplotlib` - Used for creating plots.

`seaborn` - Used for visualization.

## Contents 

This repository contains the following material:

1.  `data` contains the simulated data.
2.  `codes` contains all the scripts used for this project.
3.  `README.md`
4.  `CONTRIBUTORS.md` contains the list of the contirbutors to the project.
5.  `_quarto.yml` is a file for setting up the output directory for the reports. Keep it in the working directory to ensure that the html reports are saved in the correct folder.

## Workflow

To execute the entire pipeline, run the scripts in the following order:

1.  `generate_data.py`
2.  `render_data_quality_report.py`
3.  `clean_data.py`
4.  `render_summary_report.py`
5.  `generate_statistics.py`
6.  `generate_figure.py`

## `codes` folder

Scripts included in this project are contained in `codes` folder.

### `generate_data.py`

The script is used to generate a database of 120 subject with **Impostor Syndrome**. The dataset contains: a **resting state functional connectivity (rs-FC)** matrix for each subject, few **demographics** (age, sex), **Impostor Feeling Syndrom Scores (IFSS)** and **Anxiety Scores (AS)**. The two clinical scales have no existing reference and should not be considered in any real clinical application. To simulate a realistic processing pipeline, the dataset has been corrupted with missing/incorrect data. Higher performance anxiety is associated with higher IFSS scores, to create an opportunity to discuss confounding. In addition, the connectivity matrix has been created to provide lower FC associated to higher IFSS scores.

### `render_data_quality_report.py`

This script renders the `data_quality_report.qmd` that generates a `data_quality_report.html` in the \output folder inside the project directory. It takes as input the `participants.csv`and `connectivity_matrices.npz`. It contains a descriptive table of the participants and exploratory analysis to identify missing or corrupted data. It also provides exploratory analysis of FC matrix to identify a connectivty threshold to isolate significant connections. It detects NaN values in two variables (Age and mean_fd) and mistakes in the IFSS reported for three subjects.

### `clean_data.py`

This script takes the `participants.csv`and `connectivity_matrices.npz` as input and returns `participants_clean.csv` and `connectivity_matrices_clean.npz` as output. The script removes subjects from the original database that:

- Have a **IFSS** equal to 0.

- Have a NaN in one or more variable.

- Have a `mean_fd` higher than 0.5 mm.

In addition, it thresholds the connectivity matrix to remove all ROI to ROI correlations that are lower than 0.05.

### `render_summary_report.py`

This script takes the `participants_clean.csv` and `connectivity_matrices_clean.npz` as input and generates a `summary_report.html` in the output folder. It provides demographics and FC distribution after data cleaning and tresholding.

### `generate_statisitcs.py`

This script takes `participants_clean.csv` and `connectivity_matrices_clean.npz` as input and runs to Generalize Linear Models for each ROI-to-ROI connection to test the association between IFSS and functional connectivity. Model 1 controls for age, sex, and head motion; Model 2 additionally controls for anxiety. P-values are FDR-corrected across all connections and results are saved to results/fc_glm_results.csv.

### `generate_figure.py`

This script takes `connectivity_matrices_clean.npz` and visualizes the FC network for a selected participant as a circular graph. Positive connections are drawn in red and negative ones in blue, with edge thickness scaled by connection strength. The output is a figure in .png format that is saved to results/.

## Study reproducibility 

The synthetic database and the codes have been generated with the intent of making this project an open-access and reproducible example pipeline for anyone interested in neuroimaging and statistical analysis. The random seed is kept fixed to ensure the same synthetic dataset is generated on every run.