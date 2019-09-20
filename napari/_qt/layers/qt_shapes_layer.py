from collections import Iterable
import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QButtonGroup,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QLabel,
    QComboBox,
    QSlider,
)

from .qt_base_layer import QtLayerControls
from ...layers.shapes._constants import Mode


class QtShapesControls(QtLayerControls):
    def __init__(self, layer):
        super().__init__(layer)

        self.layer.events.mode.connect(self.set_mode)
        self.layer.events.edge_width.connect(self._on_edge_width_change)
        self.layer.events.edge_color.connect(self._on_edge_color_change)
        self.layer.events.face_color.connect(self._on_face_color_change)

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setMinimum(0)
        sld.setMaximum(40)
        sld.setSingleStep(1)
        value = self.layer.edge_width
        if isinstance(value, Iterable):
            if isinstance(value, list):
                value = np.asarray(value)
            value = value.mean()
        sld.setValue(int(value))
        sld.valueChanged[int].connect(
            lambda value=sld: self.changeWidth(value)
        )
        self.widthSlider = sld

        face_comboBox = QComboBox()
        colors = self.layer._colors
        for c in colors:
            face_comboBox.addItem(c)
        index = face_comboBox.findText(
            self.layer.face_color, Qt.MatchFixedString
        )
        if index >= 0:
            face_comboBox.setCurrentIndex(index)
        face_comboBox.activated[str].connect(
            lambda text=face_comboBox: self.changeFaceColor(text)
        )
        self.faceComboBox = face_comboBox

        edge_comboBox = QComboBox()
        colors = self.layer._colors
        for c in colors:
            edge_comboBox.addItem(c)
        index = edge_comboBox.findText(
            self.layer.edge_color, Qt.MatchFixedString
        )
        if index >= 0:
            edge_comboBox.setCurrentIndex(index)
        edge_comboBox.activated[str].connect(
            lambda text=edge_comboBox: self.changeEdgeColor(text)
        )
        self.edgeComboBox = edge_comboBox

        self.select_button = QtModeButton(
            layer, 'select', Mode.SELECT, 'Select mode'
        )
        self.direct_button = QtModeButton(
            layer, 'direct', Mode.DIRECT, 'Direct select mode'
        )
        self.panzoom_button = QtModeButton(
            layer, 'zoom', Mode.PAN_ZOOM, 'Pan/zoom mode'
        )
        self.rectangle_button = QtModeButton(
            layer, 'rectangle', Mode.ADD_RECTANGLE, 'Add rectangles'
        )
        self.ellipse_button = QtModeButton(
            layer, 'ellipse', Mode.ADD_ELLIPSE, 'Add ellipses'
        )
        self.line_button = QtModeButton(
            layer, 'line', Mode.ADD_LINE, 'Add lines'
        )
        self.path_button = QtModeButton(
            layer, 'path', Mode.ADD_PATH, 'Add paths'
        )
        self.polygon_button = QtModeButton(
            layer, 'polygon', Mode.ADD_POLYGON, 'Add polygons'
        )
        self.vertex_insert_button = QtModeButton(
            layer, 'vertex_insert', Mode.VERTEX_INSERT, 'Insert vertex'
        )
        self.vertex_remove_button = QtModeButton(
            layer, 'vertex_remove', Mode.VERTEX_REMOVE, 'Remove vertex'
        )

        self.move_front_button = QtMoveFrontButton(layer)
        self.move_back_button = QtMoveBackButton(layer)
        self.delete_button = QtDeleteShapeButton(layer)
        self.panzoom_button.setChecked(True)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.select_button)
        self.button_group.addButton(self.direct_button)
        self.button_group.addButton(self.panzoom_button)
        self.button_group.addButton(self.rectangle_button)
        self.button_group.addButton(self.ellipse_button)
        self.button_group.addButton(self.line_button)
        self.button_group.addButton(self.path_button)
        self.button_group.addButton(self.polygon_button)
        self.button_group.addButton(self.vertex_insert_button)
        self.button_group.addButton(self.vertex_remove_button)

        self.grid_layout.addWidget(self.panzoom_button, 0, 0)
        self.grid_layout.addWidget(self.select_button, 0, 1)
        self.grid_layout.addWidget(self.direct_button, 0, 2)
        self.grid_layout.addWidget(self.delete_button, 0, 3)
        self.grid_layout.addWidget(self.vertex_insert_button, 1, 0)
        self.grid_layout.addWidget(self.vertex_remove_button, 1, 1)
        self.grid_layout.addWidget(self.move_front_button, 1, 2)
        self.grid_layout.addWidget(self.move_back_button, 1, 3)
        self.grid_layout.addWidget(self.rectangle_button, 2, 0)
        self.grid_layout.addWidget(self.ellipse_button, 2, 1)
        self.grid_layout.addWidget(self.line_button, 2, 2)
        self.grid_layout.addWidget(self.path_button, 2, 3)
        self.grid_layout.addWidget(self.polygon_button, 3, 0)
        self.grid_layout.addWidget(QLabel('opacity:'), 4, 0, 1, 4)
        self.grid_layout.addWidget(self.opacitySilder, 5, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('edge width:'), 6, 0, 1, 4)
        self.grid_layout.addWidget(self.widthSlider, 7, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('blending:'), 8, 0, 1, 4)
        self.grid_layout.addWidget(self.blendComboBox, 9, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('face color:'), 10, 0, 1, 3)
        self.grid_layout.addWidget(self.faceComboBox, 11, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('edge color:'), 12, 0, 1, 3)
        self.grid_layout.addWidget(self.edgeComboBox, 13, 0, 1, 4)
        self.grid_layout.setRowStretch(14, 1)

    def mouseMoveEvent(self, event):
        self.layer.status = str(self.layer.mode)

    def set_mode(self, event):
        mode = event.mode
        if mode == Mode.SELECT:
            self.select_button.setChecked(True)
        elif mode == Mode.DIRECT:
            self.direct_button.setChecked(True)
        elif mode == Mode.PAN_ZOOM:
            self.panzoom_button.setChecked(True)
        elif mode == Mode.ADD_RECTANGLE:
            self.rectangle_button.setChecked(True)
        elif mode == Mode.ADD_ELLIPSE:
            self.ellipse_button.setChecked(True)
        elif mode == Mode.ADD_LINE:
            self.line_button.setChecked(True)
        elif mode == Mode.ADD_PATH:
            self.path_button.setChecked(True)
        elif mode == Mode.ADD_POLYGON:
            self.polygon_button.setChecked(True)
        elif mode == Mode.VERTEX_INSERT:
            self.vertex_insert_button.setChecked(True)
        elif mode == Mode.VERTEX_REMOVE:
            self.vertex_remove_button.setChecked(True)
        else:
            raise ValueError("Mode not recongnized")

    def changeFaceColor(self, text):
        self.layer.face_color = text

    def changeEdgeColor(self, text):
        self.layer.edge_color = text

    def changeWidth(self, value):
        self.layer.edge_width = float(value) / 2

    def _on_edge_width_change(self, event):
        with self.layer.events.edge_width.blocker():
            value = self.layer.edge_width
            value = np.clip(int(2 * value), 0, 40)
            self.widthSlider.setValue(value)

    def _on_edge_color_change(self, event):
        with self.layer.events.edge_color.blocker():
            index = self.edgeComboBox.findText(
                self.layer.edge_color, Qt.MatchFixedString
            )
            self.edgeComboBox.setCurrentIndex(index)

    def _on_face_color_change(self, event):
        with self.layer.events.face_color.blocker():
            index = self.faceComboBox.findText(
                self.layer.face_color, Qt.MatchFixedString
            )
            self.faceComboBox.setCurrentIndex(index)


class QtModeButton(QRadioButton):
    def __init__(self, layer, button_name, mode, tool_tip):
        super().__init__()

        self.mode = mode
        self.layer = layer
        self.setToolTip(tool_tip)
        self.setChecked(False)
        self.setProperty('mode', button_name)
        self.toggled.connect(lambda state=self: self._set_mode(state))
        self.setFixedWidth(28)

    def _set_mode(self, bool):
        with self.layer.events.mode.blocker(self._set_mode):
            if bool:
                self.layer.mode = self.mode


class QtDeleteShapeButton(QPushButton):
    def __init__(self, layer):
        super().__init__()

        self.layer = layer
        self.setFixedWidth(28)
        self.setFixedHeight(28)
        self.setToolTip('Delete selected')
        self.clicked.connect(self.layer.remove_selected)


class QtMoveBackButton(QPushButton):
    def __init__(self, layer):
        super().__init__()

        self.layer = layer
        self.setFixedWidth(28)
        self.setFixedHeight(28)
        self.setToolTip('Move to back')
        self.clicked.connect(self.layer.move_to_back)


class QtMoveFrontButton(QPushButton):
    def __init__(self, layer):
        super().__init__()

        self.layer = layer
        self.setFixedWidth(28)
        self.setFixedHeight(28)
        self.setToolTip('Move to front')
        self.clicked.connect(self.layer.move_to_front)
