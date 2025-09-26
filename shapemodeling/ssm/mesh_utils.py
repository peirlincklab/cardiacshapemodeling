import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy


def load_vtk_polydata_mesh(file_path):
    """Load a VTK PolyData mesh from a .vtk file."""
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader.GetOutput()


def calculate_distance_mesh(mesh1, mesh2):
    """Compute mean surface-to-surface distance between two meshes."""
    distance_filter = vtk.vtkDistancePolyDataFilter()
    distance_filter.SetInputData(0, mesh1)
    distance_filter.SetInputData(1, mesh2)
    distance_filter.Update()
    distances = vtk_to_numpy(distance_filter.GetOutput().GetPointData().GetArray("Distance"))
    return np.mean(np.abs(distances))