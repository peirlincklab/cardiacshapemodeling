# mesh_extraction_pipeline_single_label.py

"""
Pipeline for extracting, smoothing, and remeshing anatomical surface meshes
from a specific label in segmentation maps. 

Dependencies:
- 3D Slicer (with slicer module available in Python)
- nibabel
- numpy
- pyvista, pyacvd
"""

import os
import slicer
import vtk
import pyvista as pv
import pyacvd


def extract_and_smooth_label(input_dir, label_name="Segment_1", input_suffix=".nii.gz", output_suffix="_mesh.vtk", n_iter=100):
    print("\nExtracting and smoothing meshes from a single label...")
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(input_suffix):
                seg_file = os.path.join(root, file)
                out_file = os.path.join(root, file.replace(input_suffix, output_suffix))

                if os.path.exists(out_file):
                    print(f"Skipping {out_file}, already exists.")
                    continue

                print(f"Creating mesh from: {seg_file}")
                seg_node = slicer.util.loadSegmentation(seg_file)
                seg_node.CreateClosedSurfaceRepresentation()

                mesh = seg_node.GetClosedSurfaceInternalRepresentation(label_name)
                smoother = vtk.vtkWindowedSincPolyDataFilter()
                smoother.SetInputData(mesh)
                smoother.SetNumberOfIterations(n_iter)
                smoother.SetPassBand(0.1)
                smoother.SetNormalizeCoordinates(False)
                smoother.Update()

                writer = vtk.vtkPolyDataWriter()
                writer.SetFileName(out_file)
                writer.SetInputData(smoother.GetOutput())
                writer.Write()

                slicer.mrmlScene.Clear(0)
                print(f"Saved mesh: {out_file}")


def remesh_with_pyacvd(input_dir, target_node_count=10000, mesh_suffix="_mesh.vtk"):
    print("\nRemeshing meshes to uniform vertex count...")
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(mesh_suffix):
                file_path = os.path.join(root, file)
                print(f"Remeshing: {file_path}")
                mesh = pv.read(file_path)
                clus = pyacvd.Clustering(mesh)
                clus.subdivide(2)
                clus.cluster(target_node_count)
                remeshed = clus.create_mesh()
                remeshed.save(file_path)
                print(f"Saved remeshed mesh: {file_path}")


if __name__ == "__main__":
    input_root = "/path/to/segmentations"  # <-- change this to your designated folder

    extract_and_smooth_single_label(input_root)
    remesh_with_pyacvd(input_root)