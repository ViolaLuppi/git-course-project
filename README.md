# git-course-project

This repository contains the project produced for the course 'Open Science in Practice: Collaborative Research in Git' held in October 2026 at Karolinska Institutet.

## Purpose

The files in this repository were created to:

- Generate a dataset of subjects affected by Impostor Syndrome. The dataset contains: a resting state functional connectivity (rs-FC) matrix for each subject, few demographics (age, sex), Impostor Feeling Syndrom Scores (IFSS) and Anxiety Scores (AS). The two clinical scales do not exist in any real clinical setting and should not be considered in any real clinical application.

- Perform easy statistical analysis on the generated datasets.

- Document the process in the detail through reports.

## Resources

### Softwares

Python (3.12.15)

Quarto

#### To run the code

If it is the first time you are running the code, you can run the code from the console using:

- **if you run it for the first time**: import code.py

- **from the second time:** exec(open("path to your code").read())

### Packages

1.  Numpy: used for data structures, matrices and computation.
2.  Pandas: used to create data frames.
3.  Path: used to deal with folder paths.

## Workflow

1.  Generate the data
2.  Check the data quality
3.  Clean the data
4.  Perform statistical analysis
5.  Generate figures

## Scripts 

Scripts included in this project are:

1.  generate_data.py: used to generate the data
2.  data_quality_report.qmd: used to inspect and report data quality