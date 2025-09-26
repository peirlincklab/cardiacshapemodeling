# medoid_search.py

"""
Mesh pre-alignment and medoid search.
This script performs rigid ICP-based pre-alignment of a population of meshes
and identifies the medoid mesh (most central based on mean distance).
The code is intended to support template selection for shape modeling applications.

Dependencies:
- vtk
- pyvista
- numpy
- tqdm (for progress tracking)
"""

import os
import vtk
import numpy as np
from tqdm import tqdm
from vtk.util.numpy_support import vtk_to_numpy
import csv


def read_vtk_file(file_path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader.GetOutput()


def get_icp_transform(source, target, max_iter=100):
    icp = vtk.vtkIterativeClosestPointTransform()
    icp.SetSource(source)
    icp.SetTarget(target)
    icp.GetLandmarkTransform().SetModeToRigidBody()
    icp.SetMaximumNumberOfIterations(max_iter)
    icp.StartByMatchingCentroidsOn()
    icp.Modified()
    icp.Update()
    return icp


def apply_transform(mesh, transform):
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputData(mesh)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    return transform_filter.GetOutput()


def calculate_mean_distance(mesh1, mesh2):
    dist_filter = vtk.vtkDistancePolyDataFilter()
    dist_filter.SetInputData(0, mesh1)
    dist_filter.SetInputData(1, mesh2)
    dist_filter.Update()
    distances = vtk_to_numpy(dist_filter.GetOutput().GetPointData().GetArray("Distance"))
    return np.mean(np.abs(distances))


def pre_align_population(mesh_paths, reference_idx=0):
    print(f"\nPre-aligning {len(mesh_paths)} meshes to reference index {reference_idx}...")
    meshes = [read_vtk_file(f) for f in mesh_paths]
    ref_mesh = meshes[reference_idx]

    for mesh, path in zip(meshes, mesh_paths):
        transform = get_icp_transform(mesh, ref_mesh)
        aligned_mesh = apply_transform(mesh, transform)

        writer = vtk.vtkPolyDataWriter()
        writer.SetFileName(path)
        writer.SetInputData(aligned_mesh)
        writer.Write()
        print(f"Aligned and saved: {os.path.basename(path)}")


def find_medoid(mesh_paths, log_path="medoid_log.csv"):
    print(f"\nComputing medoid of {len(mesh_paths)} meshes...")
    meshes = [read_vtk_file(f) for f in mesh_paths]
    num_meshes = len(meshes)
    dist_matrix = np.zeros((num_meshes, num_meshes))

    print("Computing pairwise distances:")
    total_pairs = num_meshes * (num_meshes - 1) // 2
    pair_idx = 0

    with tqdm(total=total_pairs, desc="Pairwise comparisons") as pbar:
        for i in range(num_meshes):
            for j in range(i + 1, num_meshes):
                d = calculate_mean_distance(meshes[i], meshes[j])
                dist_matrix[i, j] = dist_matrix[j, i] = d
                pair_idx += 1
                pbar.update(1)

    print("Pairwise distance computation complete.")
    mean_distances = dist_matrix.mean(axis=1)
    medoid_idx = np.argmin(mean_distances)
    medoid_file = mesh_paths[medoid_idx]

    with open(log_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Mesh_File", "Mean_Distance"])
        for i, path in enumerate(mesh_paths):
            writer.writerow([os.path.basename(path), mean_distances[i]])
        writer.writerow(["Medoid", os.path.basename(medoid_file)])

    print(f"\nMedoid log saved to {log_path}")
    return medoid_file


if __name__ == "__main__":
    import glob

    input_dir = "/path/to/meshes"  # <-- Change this to the desired directory
    mesh_suffix = "mesh.vtk"     # or any pattern like "*.vtk"

    mesh_files = sorted(glob.glob(os.path.join(input_dir, f"**/*{mesh_suffix}"), recursive=True))
    print(f"Found {len(mesh_files)} mesh files.")

    pre_align_population(mesh_files)
    medoid = find_medoid(mesh_files)

    print("\nMedoid mesh:", medoid)