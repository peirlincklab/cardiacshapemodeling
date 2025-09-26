# Deformetrica Parameter Optimization Toolkit

This module provides utilities and evaluation scripts for optimizing Deformetrica model parameters for shape analysis and geodesic regression. It includes tools to select representative cohorts, configure model settings, run optimizations, and evaluate results based on reconstruction error.

---

## Contents

| File                             | Purpose                                                                 |
|----------------------------------|-------------------------------------------------------------------------|
| `optimization_cohort_selection.py` | Selects a subset of meshes for optimization via clustering or extremes |
| `deformetrica_utils.py`         | Generates Deformetrica-compatible XML configuration files               |
| `mesh_utils.py`                 | Utilities for loading VTK meshes and computing distances                |
| `parameter_optimization.ipynb`  | Notebook to run Deformetrica optimization across a parameter grid and evaluate the reconstruction error for each combination|

---

## Workflow Overview

1. **Select Optimization Cohort**
   - Choose a representative or extreme subset of meshes from your full dataset.
   - Run:
     ```bash
     python optimization_cohort_selection.py
     ```
   - Outputs a reduced cohort to the `optimization_cohort/` folder.

2. **Run Parameter Optimization**
   - Use `parameter_optimization.ipynb` to generate Deformetrica models and run models across a grid of:
     - Kernel width (ambient space stiffness)
     - Control point spacing (ambient space resolution) 
	 Given the models, the script can be used to evaluate the reconstruction error for each combination and select optimal parameters for the final model.

---

## Dependencies

- `deformetrica` (Python API)
- `vtk`, `numpy`, `pandas`, `tqdm`, `scikit-learn`
- `matplotlib`, `seaborn` (for visualization)

Install via:
```bash
pip install vtk pandas numpy tqdm scikit-learn matplotlib seaborn
```

---

## 📌 Notes

- Mesh input format: `.vtk` (PolyData)
- Matching of reconstructed and original meshes is done via subject ID in filenames.
- Directory names for each run should follow the format: `cp<value>_kw<value>`
- The script does not automatically provide the optimal parameters, but it is constructed to help the users evaluate parameters semi-automatically.

---
For issues or guidance on using Deformetrica, see: [deformetrica.org](https://www.deformetrica.org/)

