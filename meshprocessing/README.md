# Mesh Processing Tools

This directory contains scripts for processing anatomical segmentations into surface meshes suitable for statistical shape modeling. It includes mesh extraction, alignment, and medoid selection tools.

## Contents

| Script                         | Purpose                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| `mesh_extraction.py`          | Extracts, smooths, and remeshes biventricular myocardium meshes with RV dilation, given LV and RV blood pool segmentations, and LV myocardium segmentation. |
| `mesh_extraction_single_label.py` | Extracts, smooths, and remeshes meshes from a single labeled region without modifications. |
| `medoid_search.py`            | Pre-aligns a population of meshes and identifies the medoid (most central) shape. |
| `mesh_icp_alignment.py`       | Rigidly aligns meshes to a specified template using ICP, and logs the transformation matrices. |

---

## 🛠️ Dependencies

All scripts require Python 3.x and the following packages:

- `vtk`
- `nibabel`
- `numpy`
- `pyvista`
- `pyacvd`
- `scipy`
- `tqdm` (for progress tracking in medoid search)

The mesh extraction scripts rely on 3D Slicer's Python API. Please refer to 3D slicer documentation for set up and installation: https://slicer.readthedocs.io/en/latest/developer_guide/api.html.

---

## Usage Overview

### 1. Extract Meshes

For full biventricular extraction with RV dilation:

```bash
python mesh_extraction.py
```

For a single anatomical label without modification:

```bash
python mesh_extraction_single_label.py
```

Adjust paths and labels in the scripts as needed.

---

### 2. Pre-align & Find Medoid

This will align all meshes to a random reference and return the most central (medoid) mesh:

```bash
python medoid_search.py
```

The medoid can then be used as a reference for template alignment in case an idealized (or pre-established) template is not available.

---

### 3. Align Meshes to a Template

Use rigid ICP to align all meshes to a selected reference (e.g., the medoid or idealized template):

```bash
python mesh_icp_alignment.py
```

This script also writes all 4×4 ICP transformation matrices to `icp_transforms.csv`.

## 📌 Notes

- Ensure meshes are topologically and anatomically consistent before applying alignment.
- Scripts assume surface meshes are stored in `.vtk` format with consistent naming patterns. Nonetheless, the scripts are easily adaptable to other mesh formats by adjusting the VTK filters in use accordingly.
- Adapt path definitions or wrap scripts into command-line tools for better automation.

---