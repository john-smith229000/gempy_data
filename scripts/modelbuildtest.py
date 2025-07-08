"""This script demonstrates how to create a simple fault model with constant offset using GemPy,
a Python-based, open-source library for implicit geological modeling.
"""

# Import necessary libraries
import gempy as gp
from gempy.core.data import geo_model
import gempy_viewer as gpv
import numpy as np
import pyvista as pv
from gempy_engine.core.data.stack_relation_type import StackRelationType
import os
import pandas as pd
from datetime import datetime

df = pd.read_csv(r"G:\Working\Students\Undergraduate\For_Vince\Python\surface_points_final.csv")
xmin, xmax = df["X"].min(), df["X"].max()
ymin, ymax = df["Y"].min(), df["Y"].max()
zmin, zmax = df["Z"].min(), df["Z"].max()


# Create export folder if it doesn't exist

export_dir = os.path.join(os.path.expanduser("~"), "gempy_exports")
os.makedirs(export_dir, exist_ok=True)

# Export paths
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

obj_path = os.path.join(export_dir, f"gempy_model_{timestamp}.obj")
gltf_path = os.path.join(export_dir, f"gempy_model_{timestamp}.gltf")
# sphinx_gallery_thumbnail_number = 2


# %%
# Generate the model
# Define the path to data
data_path = 'https://raw.githubusercontent.com/john-smith229000/gempy_data/master/'
path_to_data = data_path + "/csv/"
# Create a GeoModel instance
buffer=100
data = gp.create_geomodel(
    project_name='fault',
    extent = [
    xmin - buffer, xmax + buffer,
    ymin - buffer, ymax + buffer,
    zmin - buffer, zmax + buffer
    ],
    refinement=6,
    importer_helper=gp.data.ImporterHelper(
        path_to_orientations=path_to_data + "orientations_final.csv",
        path_to_surface_points=path_to_data + "surface_points_final.csv"
    )
)
# Map geological series to surfaces
gp.map_stack_to_surfaces(
    gempy_model=data,
    mapping_object={
        "Strat_Series": ('rock2', 'rock1', 'rock3')
    }
)
# Define fault groups
#data.structural_frame.structural_groups[0].structural_relation = StackRelationType.FAULT
#data.structural_frame.fault_relations = np.array([[0, 1], [0, 0]])
# Compute the geological model
gp.compute_model(data)
geo_data = data

# %%
# Plot the initial geological model in the y direction
"""gpv.plot_2d(geo_data, direction=['y'], show_results=False)

# %%

# Plot the result of the model in the x and y direction with data
gpv.plot_2d(geo_data, direction='y', show_data=True)
gpv.plot_2d(geo_data, direction='x', show_data=True)




gpv.plot_3d(geo_data, show_data=True, show_boundaries=True, show_lith=True)"""



data.solutions.dc_meshes[0].dc_data
back_transformed_vertices = data.input_transform.apply_inverse(data.solutions.dc_meshes[0].vertices)
back_transformed_vertices

print("Ready to plot")
plotter = gpv.plot_3d(data, show=False)

plotter.p.export_obj(obj_path)
plotter.p.export_gltf(gltf_path)

#plotter.p.set_scale(zscale=5.0)  # exaggerate vertical scale 5x
plotter.p.show()
print("Closed and done")
