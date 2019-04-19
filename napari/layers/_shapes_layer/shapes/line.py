import numpy as np
from xml.etree.ElementTree import Element
from .shape import Shape
from ..shape_util import create_box


class Line(Shape):
    """Class for a single line segment

    Parameters
    ----------
    data : np.ndarray
        Nx2 array of vertices specifying the shape.
    edge_width : float
        thickness of lines and edges.
    edge_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    face_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    opacity : float
        Opacity of the shape, must be between 0 and 1.
    z_index : int
        Specifier of z order priority. Shapes with higher z order are displayed
        ontop of others.
    """
    def __init__(self, data, *, edge_width=1, edge_color='black',
                 face_color='white', opacity=1, z_index=0):

        super().__init__(edge_width=edge_width, edge_color=edge_color,
                         face_color=face_color, opacity=opacity,
                         z_index=z_index)
        self.data = np.array(data)
        self.name = 'line'

    @property
    def data(self):
        """np.ndarray: Nx2 array of vertices.
        """
        return self._data

    @data.setter
    def data(self, data):
        if len(data) != 2:
            raise ValueError("""Data shape does not match a line. Line
                             expects two end vertices""")
        else:
            # For line connect two points
            self._set_meshes(data, face=False, closed=False)
            self._box = create_box(data)
        self._data = data


class Path(Shape):
    """Class for a single path

    Parameters
    ----------
    data : np.ndarray
        Nx2 array of vertices specifying the shape.
    edge_width : float
        thickness of lines and edges.
    edge_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    face_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    opacity : float
        Opacity of the shape, must be between 0 and 1.
    z_index : int
        Specifier of z order priority. Shapes with higher z order are displayed
        ontop of others.
    """
    def __init__(self, data, *, edge_width=1, edge_color='black',
                 face_color='white', opacity=1, z_index=0):

        super().__init__(edge_width=edge_width, edge_color=edge_color,
                         face_color=face_color, opacity=opacity,
                         z_index=z_index)
        self.data = np.array(data)

    @property
    def data(self):
        """np.ndarray: Nx2 array of vertices.
        """
        return self._data

    @data.setter
    def data(self, data):
        if len(data) < 2:
            raise ValueError("""Data shape does not match a path. Path
                             expects at least two vertices""")
        else:
            # For path connect every all data
            self._set_meshes(data, face=False, closed=False)
            self._box = create_box(data)
        self._data = data


class Polygon(Shape):
    """Class for a single polygon

    Parameters
    ----------
    data : np.ndarray
        Nx2 array of vertices specifying the shape.
    edge_width : float
        thickness of lines and edges.
    edge_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    face_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    opacity : float
        Opacity of the shape, must be between 0 and 1.
    z_index : int
        Specifier of z order priority. Shapes with higher z order are displayed
        ontop of others.
    """
    def __init__(self, data, *, edge_width=1, edge_color='black',
                 face_color='white', opacity=1, z_index=0):

        super().__init__(edge_width=edge_width, edge_color=edge_color,
                         face_color=face_color, opacity=opacity,
                         z_index=z_index)
        self._closed = True
        self.data = np.array(data)

    @property
    def data(self):
        """np.ndarray: Nx2 array of vertices.
        """
        return self._data

    @data.setter
    def data(self, data):
        if len(data) < 2:
            raise ValueError("""Data shape does not match a polygon.
                             Polygon expects at least two vertices""")
        else:
            self._set_meshes(data)
            self._box = create_box(data)
        self._data = data

    def to_mask(self, mask_shape=None):
        """Converts the shape vertices to a boolean mask with `True` for points
        lying inside the shape. For a Line returns an array of `False` as
        a Line has no interior.

        Parameters
        ----------
        mask_shape : np.ndarray | tuple | None
            1x2 array of shape of mask to be generated. If non specified, takes
            the max of the vertiecs

        Returns
        ----------
        mask : np.ndarray
            Boolean array with `True` for points inside the shape
        """
        if mask_shape is None:
            mask_shape = self.data.max(axis=0).astype('int')

        mask = np.zeros(mask_shape, dtype=bool)

        return mask

    def to_xml(self):
        """Generates an xml element that defintes the shape according to the
        svg specification.

        Returns
        ----------
        element : Element
            xml element specifying the shape according to svg.
        """
        x = f'{self.data[0, 0]}'
        y = f'{self.data[0, 1]}'
        rx = f'{self.data[1, 0] - self.data[0, 0]}'
        ry = f'{self.data[3, 1] - self.data[0, 1]}'

        element = Element('rect', x=x, y=y, width=rx, height=ry,
                          fill='red', stroke='navy', **{'stroke-width': '10'})

        return element
