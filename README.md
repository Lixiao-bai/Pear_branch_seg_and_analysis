# Paper Title

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)]()

This repository contains the code and example data for the paper:

> **Structural Parameter Determination and Pruning Pattern Analysis of Pear Tree Shoots for Dormant Pruning**  
> Jiaqi Li, Hao Sun, Gengchen Wu, ...  
> *Plant Phenomics / 2025.  

If you use this repository in your research, please cite our paper (see [Citation](#citation)).

---

## Quick Start
### 🎥 Demo Video
https://github.com/Lixiao-bai/Pear_branch_seg_and_analysis/blob/main/demo_pipeline.mp4

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [1. Prepare Data](#1-prepare-data)
  - [2. Run the Example Pipeline](#2-run-the-example-pipeline)
  - [3. Reproduce Main Results](#3-reproduce-main-results)
- [Data Description](#data-description)
- [Results & Figures](#results--figures)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)

---

## Overview

This repository provides:

- **Implementation of the methods** proposed in our paper, including:
  - `src/data_loader.py` for loading raw and processed data.
  - `src/preprocessing.py` for data preprocessing and filtering.
  - `src/models.py` for model / algorithm implementation.
  - `src/metrics.py` for evaluation.
- **Example datasets** in `data/` to demonstrate the full pipeline.
- **Jupyter notebooks** in `notebooks/` that illustrate:
  - Data inspection and visualization.
  - Preprocessing and feature extraction.
  - Model training and evaluation.
- **Reproduction of key results** (tables and figures) reported in the paper.

> 🔎 *Note:* The dataset included in this repository is a **small subset/toy example** for demonstration.  
> For the full dataset used in the paper, please refer to [Data Description](#data-description).

---

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore

├── data/
│   ├── README.md
│   ├── sample_raw/
│   ├── sample_processed/
│   └── metadata/

├── src/
│   ├── __init__.py
│   ├── configs/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── models.py
│   ├── metrics.py
│   ├── visualization.py
│   └── utils.py

├── experiments/
│   ├── run_example.sh
│   ├── configs/
│   └── logs/

├── notebooks/
│   ├── 0_data_overview.ipynb
│   ├── 1_preprocessing_demo.ipynb
│   ├── 2_training_demo.ipynb
│   └── 3_evaluation_demo.ipynb

├── results/
│   ├── figures/
│   └── tables/

└── docs/
    ├── method_overview.md
    └── changelog.md
