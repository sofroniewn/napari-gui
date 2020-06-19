import numpy as np
from unittest.mock import patch


def test_data_change_ndisplay_image(viewer_factory):
    """Test change data calls for image layer with ndisplay change."""
    view, viewer = viewer_factory()

    np.random.seed(0)
    data = np.random.random((10, 15, 8))
    layer = viewer.add_image(data)
    visual = view.layer_to_visual[layer]

    @patch.object(
        visual, '_on_slice_data_change', wraps=visual._on_slice_data_change
    )
    def test_ndisplay_change(mocked_method, ndisplay=3):
        viewer.dims.ndisplay = ndisplay
        mocked_method.assert_called_once()

    # Switch to 3D rendering mode and back to 2D rendering mode
    test_ndisplay_change(ndisplay=3)
    test_ndisplay_change(ndisplay=2)


def test_data_change_ndisplay_labels(viewer_factory):
    """Test change data calls for labels layer with ndisplay change."""
    view, viewer = viewer_factory()

    np.random.seed(0)
    data = np.random.randint(20, size=(10, 15, 8))
    layer = viewer.add_labels(data)

    visual = view.layer_to_visual[layer]

    @patch.object(
        visual, '_on_slice_data_change', wraps=visual._on_slice_data_change
    )
    def test_ndisplay_change(mocked_method, ndisplay=3):
        viewer.dims.ndisplay = ndisplay
        mocked_method.assert_called_once()

    # Switch to 3D rendering mode and back to 2D rendering mode
    test_ndisplay_change(ndisplay=3)
    test_ndisplay_change(ndisplay=2)


def test_data_change_ndisplay_points(viewer_factory):
    """Test change data calls for points layer with ndisplay change."""
    view, viewer = viewer_factory()

    np.random.seed(0)
    data = 20 * np.random.random((10, 3))
    layer = viewer.add_points(data)
    visual = view.layer_to_visual[layer]

    @patch.object(
        visual, '_on_slice_data_change', wraps=visual._on_slice_data_change
    )
    def test_ndisplay_change(mocked_method, ndisplay=3):
        viewer.dims.ndisplay = ndisplay
        mocked_method.assert_called_once()

    # Switch to 3D rendering mode and back to 2D rendering mode
    test_ndisplay_change(ndisplay=3)
    test_ndisplay_change(ndisplay=2)


def test_data_change_ndisplay_vectors(viewer_factory):
    """Test change data calls for vectors layer with ndisplay change."""
    view, viewer = viewer_factory()

    np.random.seed(0)
    data = 20 * np.random.random((10, 2, 3))
    layer = viewer.add_vectors(data)
    visual = view.layer_to_visual[layer]

    @patch.object(
        visual, '_on_slice_data_change', wraps=visual._on_slice_data_change
    )
    def test_ndisplay_change(mocked_method, ndisplay=3):
        viewer.dims.ndisplay = ndisplay
        mocked_method.assert_called_once()

    # Switch to 3D rendering mode and back to 2D rendering mode
    test_ndisplay_change(ndisplay=3)
    test_ndisplay_change(ndisplay=2)


def test_data_change_ndisplay_shapes(viewer_factory):
    """Test change data calls for shapes layer with ndisplay change."""
    view, viewer = viewer_factory()

    np.random.seed(0)
    data = 20 * np.random.random((10, 4, 3))
    layer = viewer.add_shapes(data)

    visual = view.layer_to_visual[layer]

    @patch.object(
        visual, '_on_slice_data_change', wraps=visual._on_slice_data_change
    )
    def test_ndisplay_change(mocked_method, ndisplay=3):
        viewer.dims.ndisplay = ndisplay
        mocked_method.assert_called_once()

    # Switch to 3D rendering mode and back to 2D rendering mode
    test_ndisplay_change(ndisplay=3)
    test_ndisplay_change(ndisplay=2)


def test_data_change_ndisplay_surface(viewer_factory):
    """Test change data calls for surface layer with ndisplay change."""
    view, viewer = viewer_factory()

    np.random.seed(0)
    vertices = np.random.random((10, 3))
    faces = np.random.randint(10, size=(6, 3))
    values = np.random.random(10)
    data = (vertices, faces, values)
    layer = viewer.add_surface(data)

    visual = view.layer_to_visual[layer]

    @patch.object(
        visual, '_on_slice_data_change', wraps=visual._on_slice_data_change
    )
    def test_ndisplay_change(mocked_method, ndisplay=3):
        viewer.dims.ndisplay = ndisplay
        mocked_method.assert_called_once()

    # Switch to 3D rendering mode and back to 2D rendering mode
    test_ndisplay_change(ndisplay=3)
    test_ndisplay_change(ndisplay=2)
