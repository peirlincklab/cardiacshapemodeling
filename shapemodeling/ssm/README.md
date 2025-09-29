# 🧬 Statistical Shape Modeling (SSM)

This module performs statistical shape modeling (SSM) using mapped meshes (i.e., where point-to-point correspondence has been established). It applies rigid Procrustes alignment followed by PCA to extract dominant modes of anatomical variation.
This script is designed to be run **after** Deformetrica's LDDMM-based anatomical mapping. It assumes as input a set of consistently remeshed and topologically aligned `.vtk` surfaces (typically found in `output/DeterministicAtlas__Reconstruction__*.vtk`).

---

## 🔧 Features

- Rigid alignment using `vtkProcrustesAlignmentFilter`
- PCA on aligned mesh shapes
- Outputs:
  - `mean_shape.vtk` — average cardiac shape
  - `pc.csv` — principal shape modes (flattened)
  - `variance.csv` — eigenvalues per mode
  - `shape_coefficients.csv` — per-subject scores for selected modes
  - Optional: a cumulative variance plot as `.png`

---

## 🛠 Usage

Update and run the script directly:

```python
if __name__ == "__main__":
    run_ssm(
        input_dir="/path/to/reconstructed_vtk_meshes/",
        output_dir="/path/to/save/results/",
        image_output_path="/path/to/variance_plot.png"  # optional
    )
```

---

## 📦 Dependencies

- `vtk`
- `numpy`
- `matplotlib`
- `pandas`
- `mesh_utils.py` (for reading `.vtk` files)

---

## 📈 Output

This script generates the following files in the output directory:

| File                        | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `mean_shape.vtk`           | Average cardiac shape after alignment                                       |
| `pc.csv`                   | Principal shape modes (flattened vectors) — used for anatomical visualization |
| `variance.csv`             | Eigenvalues — variance explained by each mode                              |
| `shape_coefficients.csv`   | Per-subject shape scores — used for statistical analysis                    |
| `variance_plot.png`        | Optional plot of cumulative and per-mode variance explained                 |

> 🔍 `pc.csv` and `variance.csv` are typically used to reconstruct and visualize shape variations (e.g., ±3 SD).  
> 📊 `shape_coefficients.csv` provides quantitative shape descriptors for population-level statistical analysis.

---
---
