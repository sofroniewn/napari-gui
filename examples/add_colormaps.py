"""
Add named or unnamed vispy colormaps to existing layers.
"""

import numpy as np
import vispy.color
from skimage import data
import napari.util

histo = data.astronaut() / 255

rch, gch, bch = np.transpose(histo, (2, 0, 1))

red = vispy.color.Colormap([[0., 0., 0.], [1., 0., 0.]])
green = vispy.color.Colormap([[0., 0., 0.], [0., 1., 0.]])
blue = vispy.color.Colormap([[0., 0., 0.], [0., 0., 1.]])

with napari.util.app_context():
    v = napari.Viewer()

    rlayer = v.add_image(rch)
    rlayer.blending = 'additive'
    rlayer.Colormap = 'red', red
    glayer = v.add_image(gch)
    glayer.blending = 'additive'
    glayer.colormap = green  # this will appear as [unnamed colormap]
    blayer = v.add_image(bch)
    blayer.blending = 'additive'
    blayer.colormap = {'blue': blue}

    w = napari.Window(v)
