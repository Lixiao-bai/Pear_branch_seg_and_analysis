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

If you use this repository in academic work, please cite the paper.
🔖 [Citation](#citation) · 📄 [Paper DOI](https://doi.org/10.1016/j.plaphe.2025.100136)

---

## Demo Video

A short demo illustrating the end-to-end processing pipeline is provided:
- **Pipeline demo video**
[![Pipeline demo](results/figures/demo_preview.gif)](
https://github.com/Lixiao-bai/Pear_branch_seg_and_analysis/releases/download/video/demo_pipeline.mp4
)


---

## Overview

This repository implements the **point-cloud-based branch analysis pipeline** proposed in the paper, aiming to quantitatively characterize **dormant pruning patterns of mature pear trees**.

The main contributions supported by this codebase include:

- 3D point cloud alignment and branch structure extraction of pear trees during the dormant season.
- Quantitative measurement of structural parameters, including branch number, shoot length, and inclination angle.
- Statistical analysis of pruning patterns, demonstrating that:
  - 78.62% of annual shoots were removed,
  - 94.90% of total annual shoot length was removed,
  - pruning is dominated by thinning cuts rather than heading cuts.

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Environment](#environment)
- [Installation](#installation)
- [Usage](#usage)
- [Reproducing Paper Results](#reproducing-paper-results)
- [Data Description](#data-description)
- [Results](#results)
- [License](#license)
- [Contact](#contact)

---

## Repository Structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
│
├── data/
│   ├── README.md
│   ├── sample_raw/
│   ├── sample_processed/
│   └── metadata/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── models.py
│   ├── metrics.py
│   ├── visualization.py
│   └── utils.py
│
└── results/
    ├── figures/
    └── tables/

## Citation

If you use this code or data in your research, please cite the following paper:

```bibtex
@article{Li2025PearPruning,
  title   = {Structural parameter determination and pruning pattern analysis of pear tree shoots for dormant pruning},
  author  = {Li, Jiaqi and Sun, Hao and Wu, Gengchen and Xu, Hu and Tao, Shutian and Guo, Wei and Qi, Kaijie and Yin, Hao and Zhang, Shaoling and Ninomiya, Seishi and Mu, Yue},
  journal = {Plant Phenomics},
  year    = {2025},
  volume  = {},
  number  = {},
  pages   = {100136},
  doi     = {10.1016/j.plaphe.2025.100136}
}
