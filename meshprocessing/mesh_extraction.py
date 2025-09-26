# mesh_extraction_pipeline.py

"""
Pipeline for extracting, modifying, smoothing, and remeshing cardiac surface meshes from
segmentation label maps. Applies dilation to the RV blood pool to create an epicardial shell,
extracts a surface mesh using 3D Slicer's Python API, and remeshes it using pyacvd.

Dependencies:
- 3D Slicer (with slicer module available in Python)
- nibabel
- numpy, scipy
- pyvista, pyacvd
"""

import os
import numpy as np
import nibabel as nib
import vtk
import pyvista as pv
import pyacvd
import slicer
from scipy.ndimage import binary_dilation


def create_rv_epicardium(segmentation_data, dilation_radius_mm, voxel_spacing, padding_value=5):
    dilation_radius_voxels = [int(dilation_radius_mm / vs) for vs in voxel_spacing]
    padded_seg = np.pad(segmentation_data, padding_value, mode='constant', constant_values=0)
    rv_mask = (padded_seg == 3)
    top_slice = np.max(np.where(rv_mask)[0])

    dilated_rv = np.zeros_like(rv_mask)
    dilated_rv[:top_slice] = binary_dilation(
        rv_mask[:top_slice],
        structure=np.ones(tuple(2 * r + 1 for r in dilation_radius_voxels))
    )

    epicardial_surface = padded_seg.copy()
    epicardial_surface[(dilated_rv) & (padded_seg == 0)] = 2
    epicardial_surface[padded_seg == 3] = 3

    non_zero = np.where(epicardial_surface > 0)
    bbox = [slice(non_zero[i].min(), non_zero[i].max() + 1) for i in range(3)]
    return epicardial_surface[tuple(bbox)]


def process_segmentations(input_dir, input_suffix=".nii.gz", output_suffix="_with_epi_shell.nii.gz", dilation_radius_mm=3, padding_value=10):
    print("\nSearching for segmentation files...")
    seg_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(input_dir)
        for f in files if f.endswith(input_suffix)
    ]
    print(f"Found {len(seg_files)} files.")

    for seg_file in seg_files:
        print(f"Processing: {seg_file}")
        img = nib.load(seg_file)
        data = img.get_fdata()
        spacing = img.header.get_zooms()

        mod_data = create_rv_epicardium(data, dilation_radius_mm, spacing, padding_value)
        out_img = nib.Nifti1Image(mod_data, affine=img.affine, header=img.header)

        out_path = seg_file.replace(input_suffix, output_suffix)
        nib.save(out_img, out_path)
        print(f"Saved: {out_path}")


def extract_and_smooth_mesh(input_dir, label_name="Segment_2", input_suffix="_with_epi_shell.nii.gz", output_suffix="_mesh.vtk", n_iter=100):
    print("\nExtracting and smoothing surface meshes...")
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
    input_root = "/path/to/healthy_population"  # <-- change this

    process_segmentations(input_root)
    extract_and_smooth_mesh(input_root)
    remesh_with_pyacvd(input_root)