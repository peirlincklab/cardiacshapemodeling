# 🧊 Shape Mode Visualization

This module provides tools to visualize anatomical variability captured by the statistical shape model (SSM). It focuses on interpreting principal components (modes) obtained via PCA.

---

## Tools

| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `ssm_sd.py`        | Generates deformed meshes at ±3 standard deviations along a selected mode  |
| `ssm_animation.ipynb` | Animates shape deformation along PCA modes for dynamic visualization     |

These tools take as input the outputs of the SSM pipeline:
- `mean_shape.vtk`
- `pc.csv` (principal components)
- `variance.csv` (eigenvalues)

---

## 🛠 Usage

### Static Deformation

```bash
python ssm_sd.py
```

Customize:
- `which_mode` → selects the principal component (0 = first mode)
- `how_much_std` → magnitude of deformation (e.g. 3 = ±3 SD)

This script:
- Deforms the mean shape in ± direction
- Saves the output as `.vtk`
- Renders the three shapes (mean, +SD, –SD) using PyVista

---

### Animated Deformation

```bash
python ssm_animation.py
```

Customize:
- `which_mode`, `how_much_std`, `n_frames`, `export_animation = True`

The animation will be saved as:
``mode_<N>_animation.gif``  
(e.g., `mode_1_animation.gif`, `mode_2_animation.gif`, etc.)

This script:
- Animates smooth deformation of the mean shape along ±SD of the selected mode
- Loops the animation with pause at both extremes
- Optionally saves the animation as `.gif` or `.mp4`

## 📦 Dependencies

- `vtk`
- `numpy`
- `pyvista`
- `matplotlib`
- `itkwidgets` (optional for notebook viewing)

---

## 📁 Input Format

All inputs should be located in a `model/` directory and include:

- `mean_shape.vtk` – mean shape
- `pc.csv` – matrix of shape modes
- `variance.csv` – eigenvalues per mode

---