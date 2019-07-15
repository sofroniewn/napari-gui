"""
Display one 3-D volume layer using the add_volume API
"""

import dask.array as da
import numpy as np
from skimage import data
import napari


with napari.gui_qt():
    blobs = da.stack(
        [
            data.binary_blobs(
                length=128, blob_size_fraction=0.05, n_dim=3, volume_fraction=f
            )
            for f in np.linspace(0.05, 0.5, 10)
        ],
        axis=0,
    )
    viewer = napari.view(blobs.astype(float))
