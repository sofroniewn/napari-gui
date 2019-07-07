import numpy as np
from xml.etree.ElementTree import Element
from napari.layers import Points


def test_random_points():
    """Test instantiating Points layer with random 2D data."""
    shape = (10, 2)
    data = 20 * np.random.random(shape)
    layer = Points(data)
    assert np.all(layer.data == data)
    assert layer.ndim == shape[1]
    assert layer._data_view.ndim == 2


def test_integer_points():
    """Test instantiating Points layer with integer data."""
    shape = (10, 2)
    data = np.round(20 * np.random.random(shape)).astype(int)
    layer = Points(data)
    assert np.all(layer.data == data)
    assert layer.ndim == shape[1]
    assert layer._data_view.ndim == 2


def test_negative_points():
    """Test instantiating Points layer with negative data."""
    shape = (10, 2)
    data = 20 * np.random.random(shape) - 10
    layer = Points(data)
    assert np.all(layer.data == data)
    assert layer.ndim == shape[1]
    assert layer._data_view.ndim == 2


def test_3D_points():
    """Test instantiating Points layer with random 3D data."""
    shape = (10, 3)
    data = 20 * np.random.random(shape)
    layer = Points(data)
    assert np.all(layer.data == data)
    assert layer.ndim == shape[1]
    assert layer._data_view.ndim == 2


def test_4D_points():
    """Test instantiating Points layer with random 4D data."""
    shape = (10, 4)
    data = 20 * np.random.random(shape)
    layer = Points(data)
    assert np.all(layer.data == data)
    assert layer.ndim == shape[1]
    assert layer._data_view.ndim == 2


def test_changing_points():
    """Test changing Points data."""
    shape_a = (10, 2)
    shape_b = (20, 2)
    data_a = 20 * np.random.random(shape_a)
    data_b = 20 * np.random.random(shape_b)
    layer = Points(data_a)
    layer.data = data_b
    assert np.all(layer.data == data_b)
    assert layer.ndim == shape_b[1]
    assert layer._data_view.ndim == 2


# def test_changing_modes():
#     """Test changing modes."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.mode == 'pan_zoom'
#     assert layer.interactive == True
#
#     layer.mode = 'fill'
#     assert layer.mode == 'fill'
#     assert layer.interactive == False
#
#     layer.mode = 'paint'
#     assert layer.mode == 'paint'
#     assert layer.interactive == False
#
#     layer.mode = 'picker'
#     assert layer.mode == 'picker'
#     assert layer.interactive == False
#
#     layer.mode = 'pan_zoom'
#     assert layer.mode == 'pan_zoom'
#     assert layer.interactive == True
#
#
# def test_name():
#     """Test setting layer name."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.name == 'Labels'
#
#     layer = Labels(data, name='random')
#     assert layer.name == 'random'
#
#     layer.name = 'lbls'
#     assert layer.name == 'lbls'
#
#
# def test_seed():
#     """Test setting seed."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.seed == 0.5
#
#     layer.seed = 0.9
#     assert layer.seed == 0.9
#
#     layer = Labels(data, seed=0.7)
#     assert layer.seed == 0.7
#
#
# def test_num_colors():
#     """Test setting number of colors in colormap."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.num_colors == 50
#
#     layer.num_colors = 80
#     assert layer.num_colors == 80
#
#     layer = Labels(data, num_colors=60)
#     assert layer.num_colors == 60
#
#
# def test_colormap():
#     """Test colormap."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert type(layer.colormap) == tuple
#     assert layer.colormap[0] == 'random'
#     assert type(layer.colormap[1]) == Colormap
#
#     layer.new_colormap()
#     assert type(layer.colormap) == tuple
#     assert layer.colormap[0] == 'random'
#     assert type(layer.colormap[1]) == Colormap
#
#
# def test_metadata():
#     """Test setting labels metadata."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.metadata == {}
#
#     layer = Labels(data, metadata={'unit': 'cm'})
#     assert layer.metadata == {'unit': 'cm'}
#
#
# def test_brush_size():
#     """Test changing brush size."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.brush_size == 10
#
#     layer.brush_size = 20
#     assert layer.brush_size == 20
#
#
# def test_contiguous():
#     """Test changing contiguous."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.contiguous == True
#
#     layer.contiguous = False
#     assert layer.contiguous == False
#
#
# def test_n_dimensional():
#     """Test changing n_dimensional."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.n_dimensional == True
#
#     layer.n_dimensional = False
#     assert layer.n_dimensional == False
#
#
# def test_selecting_label():
#     """Test changing n_dimensional."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     assert layer.selected_label == 0
#     assert layer._selected_color == None
#
#     layer.selected_label = 1
#     assert layer.selected_label == 1
#     assert len(layer._selected_color) == 4
#
#
# def test_label_color():
#     """Test getting label color."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     col = layer.get_color(0)
#     assert col == None
#
#     col = layer.get_color(1)
#     assert len(col) == 4
#
#
# def test_paint():
#     """Test painting labels with different brush sizes."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     data[:10, :10] = 1
#     layer = Labels(data)
#     assert np.unique(layer.data[:5, :5]) == 1
#     assert np.unique(layer.data[5:10, 5:10]) == 1
#
#     layer.brush_size = 10
#     layer.paint([0, 0], 2)
#     assert np.unique(layer.data[:5, :5]) == 2
#     assert np.unique(layer.data[5:10, 5:10]) == 1
#
#     layer.brush_size = 20
#     layer.paint([0, 0], 2)
#     assert np.unique(layer.data[:5, :5]) == 2
#     assert np.unique(layer.data[5:10, 5:10]) == 2
#
#
# def test_fill():
#     """Test filling labels with different brush sizes."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     data[:10, :10] = 2
#     data[:5, :5] = 1
#     layer = Labels(data)
#     assert np.unique(layer.data[:5, :5]) == 1
#     assert np.unique(layer.data[5:10, 5:10]) == 2
#
#     layer.fill([0, 0], 1, 3)
#     assert np.unique(layer.data[:5, :5]) == 3
#     assert np.unique(layer.data[5:10, 5:10]) == 2
#
#
# def test_value():
#     """Test getting the value of the data at the current coordinates."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     coord, value = layer.get_value()
#     assert np.all(coord == [0, 0])
#     assert value == data[0, 0]
#
#
# def test_message():
#     """Test converting value and coords to message."""
#     data = np.round(20 * np.random.random((10, 15))).astype(int)
#     layer = Labels(data)
#     coord, value = layer.get_value()
#     msg = layer.get_message(coord, value)
#     assert type(msg) == str
#
#
# def test_thumbnail():
#     """Test the image thumbnail for square data."""
#     data = np.round(20 * np.random.random((30, 30))).astype(int)
#     layer = Labels(data)
#     layer._update_thumbnail()
#     assert layer.thumbnail.shape == layer._thumbnail_shape
#
#
# def test_xml_list():
#     """Test the xml generation."""
#     data = np.round(20 * np.random.random((30, 30))).astype(int)
#     layer = Labels(data)
#     xml = layer.to_xml_list()
#     assert type(xml) == list
#     assert len(xml) == 1
#     assert type(xml[0]) == Element
