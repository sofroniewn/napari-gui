import numpy as np

from ..utils.colormaps import ensure_colormap_tuple
from ..utils.event import Event
from ..utils.status_messages import format_float
from ..utils.validators import validate_n_seq

validate_2_tuple = validate_n_seq(2)


class IntensityVisualizationMixin:
    """A mixin that adds gamma, colormap, and contrast limits logic to Layers.

    When used, this should come before the Layer in the inheritance, e.g.:

        class Image(ImageSurfaceMixin, Layer):
            def __init__(self):
                ...
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.events.add(
            contrast_limits=Event,
            contrast_limits_range=Event,
            gamma=Event,
            colormap=Event,
        )
        self._gamma = 1
        self._colormap_name = ''
        self._contrast_limits_msg = ''
        self._contrast_limits = [None, None]
        self._contrast_limits_range = [None, None]

    def reset_contrast_limits(self):
        """Scale contrast limits to data range"""
        data_range = self._calc_data_range()
        self.contrast_limits = data_range

    def reset_contrast_limits_range(self):
        """Scale contrast limits range to data type.

        Currently, this only does something if the data type is an unsigned
        integer... otherwise it's unclear what the full range should be.
        """
        if np.issubdtype(self.dtype, np.unsignedinteger):
            info = np.iinfo(self.dtype)
            self.contrast_limits_range = (info.min, info.max)

    @property
    def colormap(self):
        """2-tuple of str, vispy.color.Colormap: colormap for luminance images.
        """
        return self._colormap_name, self._cmap

    @colormap.setter
    def colormap(self, colormap):
        self.events.colormap(colormap)

    def _on_colormap_change(self, colormap):
        name, cmap = ensure_colormap_tuple(colormap)
        self._colormap_name = name
        self._cmap = cmap
        self._update_thumbnail()

    @property
    def colormaps(self):
        """tuple of str: names of available colormaps."""
        return tuple(self._colormaps.keys())

    @property
    def contrast_limits(self):
        """list of float: Limits to use for the colormap."""
        return list(self._contrast_limits)

    @contrast_limits.setter
    def contrast_limits(self, contrast_limits):
        self.events.contrast_limits(contrast_limits)

    def _on_contrast_limits_change(self, value):
        """Set the contrast limits.

        Parameters
        ----------
        value : tuple
            Contrast limits, (min, max).
        """
        # validate_2_tuple(value)
        current_range = self.contrast_limits
        if list(value) == current_range:
            return
        self._contrast_limits = value
        self.status = format_float(value[0]) + ', ' + format_float(value[1])
        # make sure range slider is big enough to fit range
        newrange = list(self.contrast_limits_range)
        newrange[0] = min(newrange[0], value[0])
        newrange[1] = max(newrange[1], value[1])
        self.contrast_limits_range = newrange
        self._update_thumbnail()

    @property
    def contrast_limits_range(self):
        """The current valid range of the contrast limits."""
        return list(self._contrast_limits_range)

    @contrast_limits_range.setter
    def contrast_limits_range(self, contrast_limits_range):
        self.events.contrast_limits_range(contrast_limits_range)

    def _on_contrast_limits_range_change(self, value):
        """Set the valid range of the contrast limits.

        Parameters
        ----------
        value : tuple
            Valid range of contrast limits, (min, max).
        """
        # validate_2_tuple(value)
        current_range = self.contrast_limits_range
        if list(value) == current_range:
            return

        # if either value is "None", it just preserves the current range
        value = list(value)  # make sure it is mutable
        for i in range(2):
            value[i] = current_range[i] if value[i] is None else value[i]
        self._contrast_limits_range = value

        # make sure that the current values fit within the new range
        # this also serves the purpose of emitting events.contrast_limits()
        # and updating the views/controllers
        if hasattr(self, '_contrast_limits') and any(self._contrast_limits):
            cur_min, cur_max = self.contrast_limits
            new_min = min(max(value[0], cur_min), value[1])
            new_max = max(min(value[1], cur_max), value[0])
            self.contrast_limits = (new_min, new_max)

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        self.events.gamma(value)

    def _on_gamma_change(self, value):
        self.status = format_float(value)
        self._gamma = value
        self._update_thumbnail()
