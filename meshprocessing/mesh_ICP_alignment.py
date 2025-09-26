# mesh_icp_alignment.py

"""
Rigid ICP alignment of a set of meshes to a provided reference template mesh.
Each aligned mesh is written back to its original location, and all associated ICP
transformation matrices are saved in a single CSV file. 

If a pre-established or idealized reference template is not provided, please refer to medoid_search.py to find a suitable template.

Dependencies:
- vtk
- numpy
- csv
"""

import os
import numpy as np
import vtk
import csv
from vtk.util.numpy_support import vtk_to_numpy


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


def matrix_to_flat_list(vtk_matrix):
    return [vtk_matrix.GetElement(i, j) for i in range(4) for j in range(4)]


def align_meshes_to_template(mesh_paths, reference_path, transform_log_csv="icp_transforms.csv"):
    print(f"\nAligning {len(mesh_paths)} meshes to template: {reference_path}")
    reference_mesh = read_vtk_file(reference_path)

    with open(transform_log_csv, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        header = ["mesh_file"] + [f"m{i}{j}" for i in range(4) for j in range(4)]
        writer.writerow(header)

        for mesh_path in mesh_paths:
            mesh = read_vtk_file(mesh_path)
            transform = get_icp_transform(mesh, reference_mesh)

            transform_filter = vtk.vtkTransformPolyDataFilter()
            transform_filter.SetInputData(mesh)
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            writer_vtk = vtk.vtkPolyDataWriter()
            writer_vtk.SetFileName(mesh_path)
            writer_vtk.SetInputData(transform_filter.GetOutput())
            writer_vtk.Write()
            print(f"Aligned and saved: {os.path.basename(mesh_path)}")

            matrix = transform.GetMatrix()
            matrix_flat = matrix_to_flat_list(matrix)
            writer.writerow([os.path.basename(mesh_path)] + matrix_flat)

    print(f"\nAll ICP transformations saved to: {transform_log_csv}")


if __name__ == "__main__":
    import glob

    input_dir = "/path/to/meshes"  # <-- Change this to the desidered path
    reference_file = "/path/to/reference_template.vtk"  # <-- Change this to the template path
    file_suffix = "mesh.vtk"  # <-- Change this to expected suffix

    mesh_files = sorted(glob.glob(os.path.join(input_dir, f"**/*{file_suffix}"), recursive=True))
    print(f"Found {len(mesh_files)} mesh files.")

    align_meshes_to_template(mesh_files, reference_file)