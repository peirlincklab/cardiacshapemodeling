"""
Visualizes shape variation along a selected principal component (mode) of the statistical shape model.

- Loads mean shape, principal components, and eigenvalues
- Generates deformed meshes at ±N standard deviations along a selected mode
- Displays meshes using PyVista

Inputs (expected in the model directory):
- mean_shape.vtk
- pc.csv
- variance.csv

Dependencies:
- numpy
- vtk
- pyvista
- mesh_utils (custom)
"""

import os
import numpy as np
import pyvista as pv
from mesh_utils import load_vtk_polydata_mesh
from vtk.util.numpy_support import numpy_to_vtk

colors = ['#fde725', '#5ec962', '#21918c', '#3b528b', '#440154']

# === User Parameters ===
model_dir = "model"
which_mode = 0        # Index of the PCA mode (0 = first mode)
how_much_std = 3      # How many standard deviations to visualize

# === Load Inputs ===
mean_file = os.path.join(model_dir, "mean_shape.vtk")
pc_file = os.path.join(model_dir, "pc.csv")
var_file = os.path.join(model_dir, "variance.csv")

mean_mesh = load_vtk_polydata_mesh(mean_file)
mean_points = np.array([mean_mesh.GetPoint(i) for i in range(mean_mesh.GetNumberOfPoints())])

pc_matrix = np.loadtxt(pc_file, delimiter=",")
eigenvalues = np.loadtxt(var_file, delimiter=",")

# === Compute ±N SD shapes ===
std_dev = np.sqrt(eigenvalues[which_mode])
direction = pc_matrix[:, which_mode].reshape((-1, 3))

deformed_minus = mean_points - how_much_std * std_dev * direction
deformed_plus  = mean_points + how_much_std * std_dev * direction

# === Wrap into PyVista meshes ===
pv_mean = pv.PolyData(mean_points, mean_mesh.GetPolys())
pv_minus = pv.PolyData(deformed_minus, mean_mesh.GetPolys())
pv_plus = pv.PolyData(deformed_plus, mean_mesh.GetPolys())

# === Visualize ===

plotter = pv.Plotter()
plotter.add_mesh(pv_mean, color=colors[2], opacity=0.3, label="Mean Shape")
plotter.add_mesh(pv_minus, color=colors[4], label=f"- {how_much_std} SD")
plotter.add_mesh(pv_plus, color=colors[0], label=f"+ {how_much_std} SD")
plotter.add_legend()
plotter.show()
