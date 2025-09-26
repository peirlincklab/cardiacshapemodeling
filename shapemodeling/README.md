## 🧮 Statistical Shape Modeling

Once all meshes are aligned, they can be used to build a statistical shape model.

### 1. Anatomical Mapping & Correspondence

We use [Deformetrica](https://www.deformetrica.org/) to establish point-to-point correspondence across meshes via Large Deformation Diffeomorphic Metric Mapping (LDDMM).
We perform parameter optimization of the relevant hyperparameters in semi-automated bash script approach.

- **Inputs**: aligned `.vtk` meshes  
- **Outputs**: population-wide shape atlas (template mesh) and deformation parameters (momenta)

Configuration utils, bash scripts and optimization scripts are provided in `shape_modeling/deformetrica/`.  
Please refer to the [Deformetrica documentation](https://www.deformetrica.org/documentation/) for installation and usage instructions.

---

### 2. Dimensionality Reduction

We apply Principal Component Analysis (PCA) on the reconstructed meshes after anatomical mapping to extract dominant modes of variation.

- Retain the top *N* modes explaining ~90% of shape variability
- Resulting coefficients are used as shape descriptors in downstream statistical analysis

Relevant codes for PCA are provided in `shape_modeling/ssm/`

---

### 3. Outputs

- **Shape Modes** – principal directions of anatomical variation
- **Shape Coefficients** – per-subject descriptors along each mode
- **Reconstructed Meshes** – synthetic shapes at ±3 standard deviations from the mean


---

### 4. Visualization & Animation

The repository includes tools to:
- Plot distributions of shape coefficients (e.g., violin plots, scatter plots)
- Animate mesh deformation along specific modes (±3 SD range)
- Generate static or interactive 3D renderings (e.g., using PyVista or Matplotlib)

Scripts for visualization are provided in `shape_modeling/visualization/`.