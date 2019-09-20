from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QLabel,
    QComboBox,
    QSlider,
    QCheckBox,
    QButtonGroup,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
)

from .qt_base_layer import QtLayerControls
from ...layers.points._constants import Mode, Symbol


class QtPointsControls(QtLayerControls):
    def __init__(self, layer):
        super().__init__(layer)

        self.layer.events.mode.connect(self.set_mode)
        self.layer.events.n_dimensional.connect(self._on_n_dim_change)
        self.layer.events.symbol.connect(self._on_symbol_change)
        self.layer.events.size.connect(self._on_size_change)
        self.layer.events.edge_color.connect(self._on_edge_color_change)
        self.layer.events.face_color.connect(self._on_face_color_change)

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setMinimum(1)
        sld.setMaximum(100)
        sld.setSingleStep(1)
        value = self.layer.size
        sld.setValue(int(value))
        sld.valueChanged[int].connect(lambda value=sld: self.changeSize(value))
        self.sizeSlider = sld

        face_comboBox = QComboBox()
        colors = self.layer._colors
        for c in colors:
            face_comboBox.addItem(c)
        index = face_comboBox.findText(
            self.layer.face_color, Qt.MatchFixedString
        )
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
        edge_comboBox.setCurrentIndex(index)
        edge_comboBox.activated[str].connect(
            lambda text=edge_comboBox: self.changeEdgeColor(text)
        )
        self.edgeComboBox = edge_comboBox

        symbol_comboBox = QComboBox()
        for s in Symbol:
            symbol_comboBox.addItem(str(s))
        index = symbol_comboBox.findText(
            self.layer.symbol, Qt.MatchFixedString
        )
        symbol_comboBox.setCurrentIndex(index)
        symbol_comboBox.activated[str].connect(
            lambda text=symbol_comboBox: self.changeSymbol(text)
        )
        self.symbolComboBox = symbol_comboBox

        ndim_cb = QCheckBox()
        ndim_cb.setToolTip('N-dimensional points')
        ndim_cb.setChecked(self.layer.n_dimensional)
        ndim_cb.stateChanged.connect(
            lambda state=ndim_cb: self.change_ndim(state)
        )
        self.ndimCheckBox = ndim_cb

        self.select_button = QtSelectButton(layer)
        self.addition_button = QtAdditionButton(layer)
        self.panzoom_button = QtPanZoomButton(layer)
        self.delete_button = QtDeletePointsButton(layer)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.select_button)
        self.button_group.addButton(self.addition_button)
        self.button_group.addButton(self.panzoom_button)

        self.grid_layout.addWidget(self.panzoom_button, 0, 0)
        self.grid_layout.addWidget(self.select_button, 0, 1)
        self.grid_layout.addWidget(self.addition_button, 0, 2)
        self.grid_layout.addWidget(self.delete_button, 0, 3)
        self.grid_layout.addWidget(QLabel('opacity:'), 1, 0, 1, 4)
        self.grid_layout.addWidget(self.opacitySilder, 2, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('point size:'), 3, 0, 1, 4)
        self.grid_layout.addWidget(self.sizeSlider, 4, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('blending:'), 5, 0, 1, 4)
        self.grid_layout.addWidget(self.blendComboBox, 6, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('face color:'), 7, 0, 1, 3)
        self.grid_layout.addWidget(self.faceComboBox, 8, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('edge color:'), 9, 0, 1, 3)
        self.grid_layout.addWidget(self.edgeComboBox, 10, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('symbol:'), 11, 0, 1, 3)
        self.grid_layout.addWidget(self.symbolComboBox, 12, 0, 1, 4)
        self.grid_layout.addWidget(QLabel('n-dim:'), 13, 0, 1, 3)
        self.grid_layout.addWidget(self.ndimCheckBox, 13, 3)
        self.grid_layout.setRowStretch(14, 1)

    def mouseMoveEvent(self, event):
        self.layer.status = self.layer.mode

    def set_mode(self, event):
        mode = event.mode
        if mode == Mode.ADD:
            self.addition_button.setChecked(True)
        elif mode == Mode.SELECT:
            self.select_button.setChecked(True)
        elif mode == Mode.PAN_ZOOM:
            self.panzoom_button.setChecked(True)
        else:
            raise ValueError("Mode not recongnized")

    def changeFaceColor(self, text):
        self.layer.face_color = text

    def changeEdgeColor(self, text):
        self.layer.edge_color = text

    def changeSymbol(self, text):
        self.layer.symbol = text

    def changeSize(self, value):
        self.layer.size = value

    def change_ndim(self, state):
        if state == Qt.Checked:
            self.layer.n_dimensional = True
        else:
            self.layer.n_dimensional = False

    def _on_n_dim_change(self, event):
        with self.layer.events.n_dimensional.blocker():
            self.ndimCheckBox.setChecked(self.layer.n_dimensional)

    def _on_symbol_change(self, event):
        with self.layer.events.symbol.blocker():
            index = self.symbolComboBox.findText(
                self.layer.symbol, Qt.MatchFixedString
            )
            self.symbolComboBox.setCurrentIndex(index)

    def _on_size_change(self, event):
        with self.layer.events.size.blocker():
            value = self.layer.size
            self.sizeSlider.setValue(int(value))

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


class QtPanZoomButton(QRadioButton):
    def __init__(self, layer):
        super().__init__()

        self.layer = layer
        self.setToolTip('Pan/zoom mode')
        self.setChecked(True)
        self.toggled.connect(lambda state=self: self._set_mode(state))
        self.setFixedWidth(28)

    def _set_mode(self, bool):
        with self.layer.events.mode.blocker():
            if bool:
                self.layer.mode = Mode.PAN_ZOOM


class QtSelectButton(QRadioButton):
    def __init__(self, layer):
        super().__init__()

        self.layer = layer
        self.setToolTip('Select mode')
        self.setChecked(False)
        self.toggled.connect(lambda state=self: self._set_mode(state))
        self.setFixedWidth(28)

    def _set_mode(self, bool):
        with self.layer.events.mode.blocker():
            if bool:
                self.layer.mode = Mode.SELECT


class QtAdditionButton(QRadioButton):
    def __init__(self, layer):
        super().__init__()

        self.layer = layer
        self.setToolTip('Addition mode')
        self.setChecked(False)
        self.toggled.connect(lambda state=self: self._set_mode(state))
        self.setFixedWidth(28)

    def _set_mode(self, bool):
        with self.layer.events.mode.blocker():
            if bool:
                self.layer.mode = Mode.ADD


class QtDeletePointsButton(QPushButton):
    def __init__(self, layer):
        super().__init__()

        self.layer = layer
        self.setFixedWidth(28)
        self.setFixedHeight(28)
        self.setToolTip('Delete selected')
        self.clicked.connect(self.layer.remove_selected)
