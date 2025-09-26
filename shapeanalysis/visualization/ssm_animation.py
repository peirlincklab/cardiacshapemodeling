"""
Animates mesh deformation along a selected PCA mode of the statistical shape model.

- Loads mean shape, principal components, and eigenvalues
- Deforms mean mesh between ±N standard deviations
- Displays or exports animation using PyVista

Inputs (expected in the model directory):
- mean_shape.vtk
- pc.csv
- variance.csv

Dependencies:
- numpy
- pyvista
- matplotlib
- mesh_utils (custom)
"""

import os
import time
import numpy as np
import pyvista as pv
from matplotlib.cm import viridis
from mesh_utils import load_vtk_polydata_mesh

# === User Parameters ===
model_dir = "model"
which_mode = 0
n_frames = 30
how_much_std = 3
pause_at_ends = 5
export_animation = False
output_path = f"mode_{which_mode + 1}_animation.gif"  # or .mp4

# === Load Inputs ===
mean_file = os.path.join(model_dir, "mean_shape.vtk")
pc_file = os.path.join(model_dir, "pc.csv")
var_file = os.path.join(model_dir, "variance.csv")

mean_mesh = load_vtk_polydata_mesh(mean_file)
mean_points = np.array([mean_mesh.GetPoint(i) for i in range(mean_mesh.GetNumberOfPoints())])
pc_matrix = np.loadtxt(pc_file, delimiter=",")
eigenvalues = np.loadtxt(var_file, delimiter=",")

# === Compute deformation direction ===
std_dev = np.sqrt(eigenvalues[which_mode])
direction = pc_matrix[:, which_mode].reshape((-1, 3))

# === Time vector for looping animation ===
t_vals = np.linspace(-how_much_std, how_much_std, n_frames)
t_vals = np.concatenate(([t_vals[0]] * pause_at_ends, t_vals, t_vals[::-1], [t_vals[-1]] * pause_at_ends))

# === Initialize plot ===
plotter = pv.Plotter()
if export_animation:
    plotter.open_gif(output_path)

animated_mesh = pv.PolyData(mean_points, mean_mesh.GetPolys())
plotter.add_mesh(animated_mesh, color=viridis(0.6), label=f"Mode {which_mode + 1}")
plotter.add_text(f"Mode {which_mode + 1}", font_size=12)
plotter.show(auto_close=False, interactive_update=True)

# === Animation loop ===
for t in t_vals:
    animated_points = mean_points + t * std_dev * direction
    animated_mesh.points = animated_points
    plotter.render()
    if export_animation:
        plotter.write_frame()
    else:
        time.sleep(0.03)

plotter.close()
if export_animation:
    print(f"Animation saved to: {output_path}")
