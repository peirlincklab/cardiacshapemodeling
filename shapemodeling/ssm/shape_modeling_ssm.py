"""
Performs statistical shape modeling (SSM) from a set of VTK surface meshes.

Steps:
1. Load and align meshes using Procrustes alignment
2. Perform PCA on the aligned shapes
3. Save mean shape, shape modes, explained variance, and shape coefficients
4. Visualize variance explained

Dependencies:
- vtk
- numpy
- matplotlib
- pandas
- mesh_utils (custom)
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.cm import viridis
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from mesh_utils import load_vtk_polydata_mesh


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def run_ssm(input_dir, output_dir, image_output_path=None, variance_threshold=0.9, domain="shape"):
    ensure_dir(output_dir)

    mesh_files = sorted(glob.glob(os.path.join(input_dir, f"DeterministicAtlas__Reconstruction__*__subject_*.vtk")))
    print(f"Found {len(mesh_files)} mesh files.")

    meshes = [load_vtk_polydata_mesh(f) for f in mesh_files]

    # Procrustes Alignment
    group = vtk.vtkMultiBlockDataGroupFilter()
    for mesh in meshes:
        group.AddInputData(mesh)

    procrustes = vtk.vtkProcrustesAlignmentFilter()
    procrustes.SetInputConnection(group.GetOutputPort())
    procrustes.GetLandmarkTransform().SetModeToRigidBody()
    procrustes.Update()

    # Save mean shape
    mean_points = procrustes.GetMeanPoints()
    mean_shape = vtk.vtkPolyData()
    mean_shape.DeepCopy(meshes[0])
    mean_shape.SetPoints(mean_points)

    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(os.path.join(output_dir, "mean_shape.vtk"))
    writer.SetInputData(mean_shape)
    writer.Write()

    # PCA
    pca = vtk.vtkPCAAnalysisFilter()
    pca.SetInputConnection(procrustes.GetOutputPort())
    pca.Update()

    evalues = pca.GetEvals()
    modes = pca.GetOutput()
    num_modes = pca.GetModesRequiredFor(variance_threshold)
    print(f"Number of modes explaining {int(variance_threshold*100)}% variance: {num_modes}")

    # Save PCA modes as matrix
    no_points = mean_shape.GetNumberOfPoints()
    n_blocks = modes.GetNumberOfBlocks()

    modes_matrix = []
    for i in range(n_blocks):
        mode = modes.GetBlock(i)
        pts = vtk_to_numpy(mode.GetPoints().GetData())
        modes_matrix.append(pts.flatten())

    modes_matrix = np.transpose(np.array(modes_matrix))
    np.savetxt(os.path.join(output_dir, "pc.csv"), modes_matrix, delimiter=",")

    # Save explained variance
    eigenvalues = [evalues.GetValue(i) for i in range(n_blocks)]
    np.savetxt(os.path.join(output_dir, "variance.csv"), eigenvalues, delimiter=",")

    # Variance explained per mode
    total_variance = sum(eigenvalues)
    variance_explained = [(ev / total_variance) * 100 for ev in eigenvalues]
    cumulative_variance = np.cumsum(variance_explained[:30])

    for i, var in enumerate(variance_explained):
        print(f"Mode {i+1}: {var:.2f}% variance explained")

    # Save shape coefficients
    mean_pts_np = np.array([mean_shape.GetPoints().GetPoint(i) for i in range(no_points)])
    mesh_pts_np = np.array([
        np.array([m.GetPoints().GetPoint(i) for i in range(m.GetNumberOfPoints())])
        for m in meshes
    ])

    selected_modes = modes_matrix[:, :num_modes].T
    shape_coeffs = selected_modes @ (mesh_pts_np.reshape(len(meshes), -1) - mean_pts_np.flatten()).T
    shape_coeffs = shape_coeffs.T
    np.savetxt(os.path.join(output_dir, "shape_coefficients.csv"), shape_coeffs, delimiter=",")

    # Plot variance explained
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, len(variance_explained[:30]) + 1), variance_explained[:30], color='gray', label='Variance Explained')
    plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', color='black', label='Cumulative Variance')
    plt.axvline(x=8, color=viridis(0.4), linestyle='dotted', linewidth=3, label='Visualization Threshold')
    plt.axvline(x=20, color=viridis(0.8), linestyle='dotted', linewidth=3, label='Analysis Threshold')
    plt.xlabel('Mode')
    plt.ylabel('Variance Explained (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if image_output_path:
        plt.savefig(image_output_path, dpi=300)
        print(f"Saved variance plot to: {image_output_path}")
    else:
        plt.show()


if __name__ == "__main__":
    run_ssm(
        input_dir="/path/to/input",  # directory containing *.vtk meshes
        output_dir="/path/to/output",  # directory to store outputs
        image_output_path="/path/to/save/variance_plot.png"  # optional
    )
