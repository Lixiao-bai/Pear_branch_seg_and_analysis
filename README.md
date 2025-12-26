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

Abstract: *The comprehensive understanding of the dormant pruning patterns in pear trees, along with the accurate identification of shoots suitable for pruning, is essential for implementing automated pruning and fruit production. Due to the complexity of tree architecture, previous descriptions of pruning strategies were qualitative summaries based on experience. In this study, we proposed a high-precision shoot extraction pipeline through point cloud alignment at different times, enabling a quantitative analysis of the pruning patterns. The structural parameters of 126 full bearing period pear trees, encompassing two cultivars and three architectures, were characterized, including the shoot number, single shoot angle and length, as well as shoot length density. The validation results demonstrated that the method attained an R2 of 0.82, 0.92, and 0.85 for shoot number, single shoot angle and length, respectively, with mean absolute error of 18.72, 6.08°, and 0.13 ​m. The findings indicate that tree architecture exerts a greater influence on pruning compared to cultivar, particularly in Cuiguan, where significant differences were observed across diverse tree architectures. The characters of the corresponding annual (one-year-old) shoots (AS) and pruned shoots (PS) exhibit similar distribution. The AS, constituted 78.62% of the PS number, and 94.90% of length of AS were pruned, indicating that dormant pruning in full bearing period pear tree primarily targets at the annual shoots, and the pruning of annual shoots is mainly by thinning. This study could help the automatic pruning system make pruning decisions and promotes the development of fine orchard management.*


If you use this repository in academic work, please cite the paper.
🔖 [Citation](#citation) · 📄 [Paper DOI](https://doi.org/10.1016/j.plaphe.2025.100136)

---

## Demo Video

A short demo illustrating the processing pipeline is provided:
- **Pipeline demo video**
https://github.com/Lixiao-bai/Pear_branch_seg_and_analysis/releases/download/video/demo_pipeline.mp4

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
- [Data Description](#data-description)
- [Usage](#usage)
- [License](#license)
- [Citation](#citation)


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
│   └── sample_processed/
│
├── src/
│   ├── Registration.py
│   ├── Distance_filter&cluster.py
│   ├── parameters_measurement.py
│   ├── Get_new&pruned.py
│   └── utils.py
│
└── results/
    ├── figures/
    └── tables/
```

## Environment

**Operating System:**
	- Ubuntu 20.04 / 22.04
	- Windows 10 / 11
	- Mac OS
**Python:**
	- Python 3.9 or higher 
**Python Package Manager:**
	- Miniconda(recommended)

Notes:
	The code is OS-independent and does not rely on platform-specific binaries.


## Installation

We recommend using **Miniconda** to manage the Python environment and dependencies.

### 1. Create a Conda environment

    conda create -n my_env python=3.9 -y
    conda activate my_env

You may change the environment name (`my_env`) or the Python version (≥ 3.9) if needed.

### 2. Install required Python packages

Make sure you are in the project root directory, then run:

    pip install -r requirements.txt

This will install all required third-party libraries, including NumPy, SciPy, Open3D, scikit-learn, and point cloud processing utilities.

### Notes

- Installing **pc-skeletor** may fail in some environments due to dependency incompatibilities (most commonly related to NumPy versions).
- If you encounter installation errors, please try **downgrading NumPy**  and then **download the source package from PyPI and install it locally**.
  
## Data-description
```text

```

## Usage



## Citation

If you use this code or data in your research, please cite the following paper:

```bibtex
@article{Li2025PearPruning,
  title   = {Structural parameter determination and pruning pattern analysis of pear tree shoots for dormant pruning},
  author  = {Jiaqi Li, Hao Sun, Gengchen Wu, Hu Xu, Shutian Tao, Wei Guo, Kaijie Qi, Hao Yin, Shaoling Zhang, Seishi Ninomiya, Yue Mu},
  journal = {Plant Phenomics},
  year    = {2025},
  volume  = {7},
  issue  = {4},
  pages   = {100136},
  doi     = {10.1016/j.plaphe.2025.100136}
}
```

## License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software for academic and commercial purposes, provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the software.
