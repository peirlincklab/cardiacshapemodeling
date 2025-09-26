# optimization_cohort_selection.py

"""
Select representative or extreme shapes from a mesh cohort for parameter optimization in Deformetrica.
Supports two strategies:
- Cluster-based sampling (chooses center of K clusters)
- Distance-based extremes (chooses top-N farthest from template)

Dependencies:
- vtk
- numpy
- pandas
- scikit-learn
- tqdm
"""

import os
import glob
import shutil
import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm
import vtk
from vtk.util.numpy_support import vtk_to_numpy


def load_vtk_polydata_mesh(file_path):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader.GetOutput()


def calculate_distance_mesh(mesh1, mesh2):
    dist_filter = vtk.vtkDistancePolyDataFilter()
    dist_filter.SetInputData(0, mesh1)
    dist_filter.SetInputData(1, mesh2)
    dist_filter.Update()
    distances = vtk_to_numpy(dist_filter.GetOutput().GetPointData().GetArray("Distance"))
    return np.mean(np.abs(distances))


def compute_distances(reference_mesh, mesh_files):
    print("\nComputing distances to reference mesh...")
    distances = []
    for file in tqdm(mesh_files, desc="Distance calculation"):
        mesh = load_vtk_polydata_mesh(file)
        dist = calculate_distance_mesh(reference_mesh, mesh)
        distances.append(dist)
    return np.array(distances)


def select_representative_meshes(distance_matrix, mesh_files, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(distance_matrix.reshape(-1, 1))
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    representative_indices = []
    for i in range(n_clusters):
        cluster_idx = np.where(labels == i)[0]
        dists = np.linalg.norm(distance_matrix[cluster_idx] - centers[i], axis=1)
        closest_idx = cluster_idx[np.argmin(dists)]
        representative_indices.append(closest_idx)

    return [mesh_files[i] for i in representative_indices]


def select_extreme_meshes(distance_matrix, mesh_files, top_n=10):
    indices = np.argsort(-distance_matrix)[:top_n]
    return [mesh_files[i] for i in indices]


def copy_selected_meshes(selected_files, output_dir="optimization_cohort"):
    os.makedirs(output_dir, exist_ok=True)
    for file in selected_files:
        shutil.copy(file, os.path.join(output_dir, os.path.basename(file)))
    print(f"\nCopied {len(selected_files)} files to: {output_dir}")


if __name__ == "__main__":
    # --- USER INPUT SECTION ---
    strategy = "clustering"  # Options: "clustering" or "extreme"
    reference_file = "/path/to/template.vtk"
    input_dir = "/path/to/mesh_directory"
    file_pattern = "*epicardium_shell.vtk"
    n_clusters = 5
    n_extremes = 15
    output_dir = "optimization_cohort"

    # --- RUN SELECTION ---
    mesh_files = glob.glob(os.path.join(input_dir, file_pattern))
    reference_mesh = load_vtk_polydata_mesh(reference_file)
    distances = compute_distances(reference_mesh, mesh_files)

    if strategy == "clustering":
        print("\nSelecting most representative meshes (cluster centers)...")
        selected = select_representative_meshes(distances, mesh_files, n_clusters=n_clusters)
    elif strategy == "extreme":
        print("\nSelecting most extreme meshes (farthest from reference)...")
        selected = select_extreme_meshes(distances, mesh_files, top_n=n_extremes)
    else:
        raise ValueError("Unsupported strategy: choose 'clustering' or 'extreme'")

    for f in selected:
        print(f)

    copy_selected_meshes(selected, output_dir=output_dir)