# Structural Parameter Determination and Pruning Pattern Analysis of Pear Tree Shoots for Dormant Pruning

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](#installation)
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.plaphe.2025.100136-blue)](https://doi.org/10.1016/j.plaphe.2025.100136)

This repository provides the **code implementation and example data** for the paper:

> **Structural parameter determination and pruning pattern analysis of pear tree shoots for dormant pruning**  
> Jiaqi Li, Hao Sun, Gengchen Wu, Hu Xu, Shutian Tao, Wei Guo, Kaijie Qi, Hao Yin,  
> Shaoling Zhang, Seishi Ninomiya, Yue Mu  
> *Plant Phenomics*, 2025, Article 100136  
> DOI: https://doi.org/10.1016/j.plaphe.2025.100136

If you use this repository in academic work, please cite the paper (see [Citation](#citation)).

---

## Demo Video

A short demo illustrating the end-to-end processing pipeline is provided:

- **Pipeline demo video**  
  https://github.com/Lixiao-bai/Pear_branch_seg_and_analysis/blob/main/demo_pipeline.mp4



  

---

## Overview

This repository implements the **point-cloud-based branch analysis pipeline** proposed in the paper, aiming to quantitatively characterize **dormant pruning patterns of mature pear trees**.

The main contributions supported by this codebase include:

- **3D point cloud alignment and branch structure extraction** of pear trees during the dormant season.
- **Quantitative measurement of structural parameters**, including:
  - branch (shoot) number,
  - shoot length,
  - shoot inclination angle,
  - length distribution and density.
- **Statistical analysis of pruning patterns**, revealing that:
  - **78.62% of annual shoots** were removed by pruning,
  - **94.90% of total annual shoot length** was removed,
  - pruning behavior is dominated by **thinning cuts rather than heading cuts**,
  - tree architecture has a stronger influence on pruning strategy than cultivar.

The pipeline is designed to support **objective pruning evaluation**, with potential applications in **automated pruning systems and precision orchard management**.

> **Important note**  
> The data included in this repository is a **small demonstration subset** for reproducibility and code inspection.  
> It does **not** represent the full experimental dataset reported in the paper.

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Environment](#environment)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Reproducing Paper Results](#reproducing-paper-results)
- [Data Description](#data-description)
- [Results](#results)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

---

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md
│   ├── sample_raw/          # example raw point cloud data
│   ├── sample_processed/    # processed point clouds / intermediates
│   └── metadata/            # metadata and configuration files
│
├── src/
│   ├── __init__.py
│   ├── configs/
│   ├── data_loader.py       # data loading utilities
│   ├── preprocessing.py    # filtering and preprocessing
│   ├── models.py            # branch extraction / analysis methods
│   ├── metrics.py           # evaluation metrics
│   ├── visualization.py    # plotting and visualization
│   └── utils.py
│
├── experiments/
│   ├── run_example.sh       # example pipeline entry
│   ├── configs/
│   └── logs/
│
├── notebooks/
│   ├── 0_data_overview.ipynb
│   ├── 1_preprocessing_demo.ipynb
│   ├── 2_training_demo.ipynb
│   └── 3_evaluation_demo.ipynb
│
├── results/
│   ├── figures/
│   └── tables/
│
└── docs/
    ├── method_overview.md
    └── changelog.md

@article{Li2025PearDormantPruning,
  title   = {Structural parameter determination and pruning pattern analysis of pear tree shoots for dormant pruning},
  author  = {Li, Jiaqi and Sun, Hao and Wu, Gengchen and Xu, Hu and Tao, Shutian and Guo, Wei and Qi, Kaijie and Yin, Hao and Zhang, Shaoling and Ninomiya, Seishi and Mu, Yue},
  journal = {Plant Phenomics},
  year    = {2025},
  volume  = {7},
  pages   = {100136},
  doi     = {10.1016/j.plaphe.2025.100136}
}
