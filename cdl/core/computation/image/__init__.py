# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
.. Image computation objects (see parent package :mod:`cdl.core.computation`)
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import guidata.dataset as gds
import numpy as np
import scipy.ndimage as spi
import scipy.signal as sps
from plotpy.mathutils.geometry import vector_rotation
from skimage import filters

from cdl.algorithms.image import (
    BINNING_OPERATIONS,
    binning,
    flatfield,
    get_centroid_fourier,
    get_enclosing_circle,
    get_hough_circle_peaks,
    z_fft,
    z_ifft,
)
from cdl.config import _
from cdl.core.computation.base import (
    ClipParam,
    FFTParam,
    GaussianParam,
    MovingAverageParam,
    MovingMedianParam,
    ThresholdParam,
)
from cdl.core.model.base import BaseProcParam
from cdl.core.model.image import ImageObj, RoiDataGeometries, RoiDataItem
from cdl.core.model.signal import SignalObj

VALID_DTYPES_STRLIST = ImageObj.get_valid_dtypenames()


def dst_11(src: ImageObj, name: str, suffix: str | None = None) -> ImageObj:
    """Create result image object for compute_11 function

    Args:
        src (ImageObj): input image object
        name (str): name of the processing function

    Returns:
        ImageObj: output image object
    """
    dst = src.copy(title=f"{name}({src.short_id})")
    if suffix is not None:
        dst.title += "|" + suffix
    return dst


def dst_11_signal(src: ImageObj, name: str, suffix: str | None = None) -> SignalObj:
    """Create result signal object for compute_11 function

    Args:
        src (ImageObj): input image object
        name (str): name of the processing function

    Returns:
        SignalObj: output signal object
    """
    title = f"{name}({src.short_id})"
    dst = SignalObj(title=title)
    dst.title = title
    if suffix is not None:
        dst.title += "|" + suffix
    return dst


def dst_n1n(
    src1: ImageObj, src2: ImageObj, name: str, suffix: str | None = None
) -> ImageObj:
    """Create result image object for compute_n1n function

    Args:
        src1 (ImageObj): input image object
        src2 (ImageObj): input image object
        name (str): name of the processing function

    Returns:
        ImageObj: output image object
    """
    dst = src1.copy(title=f"{name}({src1.short_id}, {src2.short_id})")
    if suffix is not None:
        dst.title += "|" + suffix
    return dst


# -------- compute_n1 functions --------------------------------------------------------
# Functions with N input images and 1 output image
# --------------------------------------------------------------------------------------
# Those functions are perfoming a computation on N input images and return a single
# output image. If we were only executing these functions locally, we would not need
# to define them here, but since we are using the multiprocessing module, we need to
# define them here so that they can be pickled and sent to the worker processes.
# Also, we need to systematically return the output image object, even if it is already
# modified in place, because the multiprocessing module will not be able to retrieve
# the modified object from the worker processes.


def compute_add(dst: ImageObj, src: ImageObj) -> ImageObj:
    """Compute addition between two images

    Args:
        dst (ImageObj): output image object
        src (ImageObj): input image object
    """
    dst.data += np.array(src.data, dtype=dst.data.dtype)
    return dst


def compute_product(dst: ImageObj, src: ImageObj) -> ImageObj:
    """Compute product between two images

    Args:
        dst (ImageObj): output image object
        src (ImageObj): input image object
    """
    dst.data *= np.array(src.data, dtype=dst.data.dtype)
    return dst


# -------- compute_n1n functions -------------------------------------------------------
# Functions with N input images + 1 input image and N output images
# --------------------------------------------------------------------------------------


def compute_difference(src1: ImageObj, src2: ImageObj) -> ImageObj:
    """Compute difference between two images
    Args:
        src1 (ImageObj): input image object
        src2 (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_n1n(src1, src2, "difference")
    dst.data = src1.data - src2.data
    return dst


def compute_quadratic_difference(src1: ImageObj, src2: ImageObj) -> ImageObj:
    """Compute quadratic difference between two images
    Args:
        src1 (ImageObj): input image object
        src2 (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_n1n(src1, src2, "quadratic_difference")
    dst.data = (src1.data - src2.data) / np.sqrt(2.0)
    if np.issubdtype(dst.data.dtype, np.unsignedinteger):
        dst.data[src1.data < src2.data] = 0
    return dst


def compute_division(src1: ImageObj, src2: ImageObj) -> ImageObj:
    """Compute division between two images
    Args:
        src1 (ImageObj): input image object
        src2 (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_n1n(src1, src2, "division")
    dst.data = src1.data / np.array(src2.data, dtype=src1.data.dtype)
    return dst


class FlatFieldParam(BaseProcParam):
    """Flat-field parameters"""

    threshold = gds.FloatItem(_("Threshold"), default=0.0)


def compute_flatfield(src1: ImageObj, src2: ImageObj, p: FlatFieldParam) -> ImageObj:
    """Compute flat field correction
    Args:
        src1 (ImageObj): raw data image object
        src2 (ImageObj): flat field image object
        p (FlatFieldParam): flat field parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_n1n(src1, src2, "flatfield", f"threshold={p.threshold}")
    dst.data = flatfield(src1.data, src2.data, p.threshold)
    return dst


# -------- compute_11 functions --------------------------------------------------------
# Functions with 1 input image and 1 output image
# --------------------------------------------------------------------------------------


class LogP1Param(gds.DataSet):
    """Log10 parameters"""

    n = gds.FloatItem("n")


def compute_logp1(src: ImageObj, p: LogP1Param) -> ImageObj:
    """Compute log10(z+n)
    Args:
        src (ImageObj): input image object
        p (LogP1Param): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "log_z_plus_n", f"n={p.n}")
    dst.data = np.log10(src.data + p.n)
    return dst


class RotateParam(gds.DataSet):
    """Rotate parameters"""

    boundaries = ("constant", "nearest", "reflect", "wrap")
    prop = gds.ValueProp(False)

    angle = gds.FloatItem(f"{_('Angle')} (°)")
    mode = gds.ChoiceItem(
        _("Mode"), list(zip(boundaries, boundaries)), default=boundaries[0]
    )
    cval = gds.FloatItem(
        _("cval"),
        default=0.0,
        help=_(
            "Value used for points outside the "
            "boundaries of the input if mode is "
            "'constant'"
        ),
    )
    reshape = gds.BoolItem(
        _("Reshape the output array"),
        default=False,
        help=_(
            "Reshape the output array "
            "so that the input array is "
            "contained completely in the output"
        ),
    )
    prefilter = gds.BoolItem(_("Prefilter the input image"), default=True).set_prop(
        "display", store=prop
    )
    order = gds.IntItem(
        _("Order"),
        default=3,
        min=0,
        max=5,
        help=_("Spline interpolation order"),
    ).set_prop("display", active=prop)


def rotate_obj_coords(
    angle: float, obj: ImageObj, orig: ImageObj, coords: np.ndarray
) -> None:
    """Apply rotation to coords associated to image obj
    Args:
        angle (float): rotation angle (in degrees)
        obj (ImageObj): image object
        orig (ImageObj): original image object
        coords (numpy.ndarray): coordinates to rotate
    Returns:
        np.ndarray: output data
    """
    for row in range(coords.shape[0]):
        for col in range(0, coords.shape[1], 2):
            x1, y1 = coords[row, col : col + 2]
            dx1 = x1 - orig.xc
            dy1 = y1 - orig.yc
            dx2, dy2 = vector_rotation(-angle * np.pi / 180.0, dx1, dy1)
            coords[row, col : col + 2] = dx2 + obj.xc, dy2 + obj.yc
    obj.roi = None


def rotate_obj_alpha(
    obj: ImageObj, orig: ImageObj, coords: np.ndarray, p: RotateParam
) -> None:
    """Apply rotation to coords associated to image obj"""
    rotate_obj_coords(p.angle, obj, orig, coords)


def compute_rotate(src: ImageObj, p: RotateParam) -> ImageObj:
    """Rotate data
    Args:
        src (ImageObj): input image object
        p (RotateParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "rotate", f"α={p.angle:.3f}°, mode='{p.mode}'")
    dst.data = spi.rotate(
        src.data,
        p.angle,
        reshape=p.reshape,
        order=p.order,
        mode=p.mode,
        cval=p.cval,
        prefilter=p.prefilter,
    )
    dst.transform_shapes(src, rotate_obj_alpha, p)
    return dst


def rotate_obj_90(dst: ImageObj, src: ImageObj, coords: np.ndarray) -> None:
    """Apply rotation to coords associated to image obj"""
    rotate_obj_coords(90.0, dst, src, coords)


def compute_rotate90(src: ImageObj) -> ImageObj:
    """Rotate data 90°
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "rotate90")
    dst.data = np.rot90(src.data)
    dst.transform_shapes(src, rotate_obj_90)
    return dst


def rotate_obj_270(dst: ImageObj, src: ImageObj, coords: np.ndarray) -> None:
    """Apply rotation to coords associated to image obj"""
    rotate_obj_coords(270.0, dst, src, coords)


def compute_rotate270(src: ImageObj) -> ImageObj:
    """Rotate data 270°
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "rotate270")
    dst.data = np.rot90(src.data, 3)
    dst.transform_shapes(src, rotate_obj_270)
    return dst


# pylint: disable=unused-argument
def hflip_coords(dst: ImageObj, src: ImageObj, coords: np.ndarray) -> None:
    """Apply HFlip to coords"""
    coords[:, ::2] = dst.x0 + dst.dx * dst.data.shape[1] - coords[:, ::2]
    dst.roi = None


def compute_fliph(src: ImageObj) -> ImageObj:
    """Flip data horizontally
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "fliph")
    dst.data = np.fliplr(src.data)
    dst.transform_shapes(src, hflip_coords)
    return dst


# pylint: disable=unused-argument
def vflip_coords(dst: ImageObj, src: ImageObj, coords: np.ndarray) -> None:
    """Apply VFlip to coords"""
    coords[:, 1::2] = dst.y0 + dst.dy * dst.data.shape[0] - coords[:, 1::2]
    dst.roi = None


def compute_flipv(src: ImageObj) -> ImageObj:
    """Flip data vertically
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "flipv")
    dst.data = np.flipud(src.data)
    dst.transform_shapes(src, vflip_coords)
    return dst


class GridParam(gds.DataSet):
    """Grid parameters"""

    _prop = gds.GetAttrProp("direction")
    _directions = (("col", _("columns")), ("row", _("rows")))
    direction = gds.ChoiceItem(_("Distribute over"), _directions, radio=True).set_prop(
        "display", store=_prop
    )
    cols = gds.IntItem(_("Columns"), default=1, nonzero=True).set_prop(
        "display", active=gds.FuncProp(_prop, lambda x: x == "col")
    )
    rows = gds.IntItem(_("Rows"), default=1, nonzero=True).set_prop(
        "display", active=gds.FuncProp(_prop, lambda x: x == "row")
    )
    colspac = gds.FloatItem(_("Column spacing"), default=0.0, min=0.0)
    rowspac = gds.FloatItem(_("Row spacing"), default=0.0, min=0.0)


class ResizeParam(gds.DataSet):
    """Resize parameters"""

    boundaries = ("constant", "nearest", "reflect", "wrap")
    prop = gds.ValueProp(False)

    zoom = gds.FloatItem(_("Zoom"))
    mode = gds.ChoiceItem(
        _("Mode"), list(zip(boundaries, boundaries)), default=boundaries[0]
    )
    cval = gds.FloatItem(
        _("cval"),
        default=0.0,
        help=_(
            "Value used for points outside the "
            "boundaries of the input if mode is "
            "'constant'"
        ),
    )
    prefilter = gds.BoolItem(_("Prefilter the input image"), default=True).set_prop(
        "display", store=prop
    )
    order = gds.IntItem(
        _("Order"),
        default=3,
        min=0,
        max=5,
        help=_("Spline interpolation order"),
    ).set_prop("display", active=prop)


def compute_resize(src: ImageObj, p: ResizeParam) -> ImageObj:
    """Zooming function
    Args:
        src (ImageObj): input image object
        p (ResizeParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "resize", f"zoom={p.zoom:.3f}")
    dst.data = spi.interpolation.zoom(
        src.data,
        p.zoom,
        order=p.order,
        mode=p.mode,
        cval=p.cval,
        prefilter=p.prefilter,
    )
    if dst.dx is not None and dst.dy is not None:
        dst.dx, dst.dy = dst.dx / p.zoom, dst.dy / p.zoom
    return dst


class BinningParam(gds.DataSet):
    """Binning parameters"""

    binning_x = gds.IntItem(
        _("Cluster size (X)"),
        default=2,
        min=2,
        help=_("Number of adjacent pixels to be combined together along X-axis."),
    )
    binning_y = gds.IntItem(
        _("Cluster size (Y)"),
        default=2,
        min=2,
        help=_("Number of adjacent pixels to be combined together along Y-axis."),
    )
    _operations = BINNING_OPERATIONS
    operation = gds.ChoiceItem(
        _("Operation"),
        list(zip(_operations, _operations)),
        default=_operations[0],
    )
    _dtype_list = ["dtype"] + VALID_DTYPES_STRLIST
    dtype_str = gds.ChoiceItem(
        _("Data type"),
        list(zip(_dtype_list, _dtype_list)),
        help=_("Output image data type."),
    )
    change_pixel_size = gds.BoolItem(
        _("Change pixel size"),
        default=False,
        help=_("Change pixel size so that overall image size remains the same."),
    )


def compute_binning(src: ImageObj, param: BinningParam) -> ImageObj:
    """Binning function on data
    Args:
        src (ImageObj): input image object
        param (BinningParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(
        src,
        "binning",
        f"{param.binning_x}x{param.binning_y},{param.operation},"
        f"change_pixel_size={param.change_pixel_size}",
    )
    dst.data = binning(
        src.data,
        binning_x=param.binning_x,
        binning_y=param.binning_y,
        operation=param.operation,
        dtype=None if param.dtype_str == "dtype" else param.dtype_str,
    )
    if param.change_pixel_size:
        if src.dx is not None and src.dy is not None:
            dst.dx = src.dx * param.binning_x
            dst.dy = src.dy * param.binning_y
    else:
        # TODO: [P2] Instead of removing geometric shapes, apply zoom
        dst.remove_all_shapes()
    return dst


def extract_multiple_roi(src: ImageObj, group: gds.DataSetGroup) -> ImageObj:
    """Extract multiple regions of interest from data
    Args:
        src (ImageObj): input image object
        group (gds.DataSetGroup): parameters defining the regions of interest
    Returns:
        ImageObj: output image object
    """
    x0 = max(min(p.x0 for p in group.datasets), 0)
    y0 = max(min(p.y0 for p in group.datasets), 0)
    x1 = max(p.x1 for p in group.datasets)
    y1 = max(p.y1 for p in group.datasets)
    suffix = None
    if len(group.datasets) == 1:
        p = group.datasets[0]
        suffix = p.get_suffix()
    dst = dst_11(src, "extract_multiple_roi", suffix)
    dst.x0 += x0 * src.dx
    dst.y0 += y0 * src.dy
    dst.roi = None
    if len(group.datasets) == 1:
        dst.data = src.data.copy()[y0:y1, x0:x1]
        return dst
    out = np.zeros_like(src.data)
    for p in group.datasets:
        slice1, slice2 = slice(max(p.y0, 0), p.y1 + 1), slice(max(p.x0, 0), p.x1 + 1)
        out[slice1, slice2] = src.data[slice1, slice2]
    dst.data = out[y0:y1, x0:x1]
    return dst


def extract_single_roi(src: ImageObj, p: gds.DataSet) -> ImageObj:
    """Extract single ROI
    Args:
        src (ImageObj): input image object
        p (gds.DataSet): ROI parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "extract_single_roi", p.get_suffix())
    x0, y0, x1, y1 = max(p.x0, 0), max(p.y0, 0), p.x1, p.y1
    dst.data = src.data.copy()[y0:y1, x0:x1]
    dst.x0 += x0 * src.dx
    dst.y0 += y0 * src.dy
    dst.roi = None
    if p.geometry is RoiDataGeometries.CIRCLE:
        # Circular ROI
        dst.roi = p.get_single_roi()
    return dst


class ProfileParam(gds.DataSet):
    """Horizontal or vertical profile parameters"""

    _prop = gds.GetAttrProp("direction")
    _directions = (("horizontal", _("horizontal")), ("vertical", _("vertical")))
    direction = gds.ChoiceItem(_("Direction"), _directions, radio=True).set_prop(
        "display", store=_prop
    )
    row = gds.IntItem(_("Row"), default=0, min=0).set_prop(
        "display", active=gds.FuncProp(_prop, lambda x: x == "horizontal")
    )
    col = gds.IntItem(_("Column"), default=0, min=0).set_prop(
        "display", active=gds.FuncProp(_prop, lambda x: x == "vertical")
    )


def compute_profile(src: ImageObj, p: ProfileParam) -> ImageObj:
    """Compute horizontal or vertical profile
    Args:
        src: input image object
        p: parameters
    Returns:
        Output image object
    """
    p.row = min(p.row, src.data.shape[0] - 1)
    p.col = min(p.col, src.data.shape[1] - 1)
    if p.direction == "horizontal":
        suffix = f"row={p.row}"
        x, y = np.arange(src.data.shape[1]), np.array(src.data[p.row, :], dtype=float)
    else:
        suffix = f"col={p.col}"
        x, y = np.arange(src.data.shape[0]), np.array(src.data[:, p.col], dtype=float)
    dst = dst_11_signal(src, "profile", suffix)
    dst.set_xydata(x, y)
    return dst


class AverageProfileParam(gds.DataSet):
    """Average horizontal or vertical profile parameters"""

    _directions = (("horizontal", _("horizontal")), ("vertical", _("vertical")))
    direction = gds.ChoiceItem(_("Direction"), _directions, radio=True)
    _hgroup_begin = gds.BeginGroup(_("Profile rectangular area"))
    row1 = gds.IntItem(_("Row 1"), default=0, min=0)
    row2 = gds.IntItem(_("Row 2"), default=-1, min=-1)
    col1 = gds.IntItem(_("Column 1"), default=0, min=0)
    col2 = gds.IntItem(_("Column 2"), default=-1, min=-1)
    _hgroup_end = gds.EndGroup(_("Profile rectangular area"))


def compute_average_profile(src: ImageObj, p: AverageProfileParam) -> ImageObj:
    """Compute horizontal or vertical average profile
    Args:
        src: input image object
        p: parameters
    Returns:
        Output image object
    """
    if p.row2 == -1:
        p.row2 = src.data.shape[0] - 1
    if p.col2 == -1:
        p.col2 = src.data.shape[1] - 1
    if p.row1 > p.row2:
        p.row1, p.row2 = p.row2, p.row1
    if p.col1 > p.col2:
        p.col1, p.col2 = p.col2, p.col1
    p.row1 = min(p.row1, src.data.shape[0] - 1)
    p.row2 = min(p.row2, src.data.shape[0] - 1)
    p.col1 = min(p.col1, src.data.shape[1] - 1)
    p.col2 = min(p.col2, src.data.shape[1] - 1)
    suffix = f"{p.direction}, rows=[{p.row1}, {p.row2}], cols=[{p.col1}, {p.col2}]"
    if p.direction == "horizontal":
        x = np.arange(p.col1, p.col2 + 1)
        y = np.mean(src.data[p.row1 : p.row2 + 1, p.col1 : p.col2 + 1], axis=0)
    else:
        x = np.arange(p.row1, p.row2 + 1)
        y = np.mean(src.data[p.row1 : p.row2 + 1, p.col1 : p.col2 + 1], axis=1)
    dst = dst_11_signal(src, "average_profile", suffix)
    dst.set_xydata(x, y)
    return dst


def compute_swap_axes(src: ImageObj) -> ImageObj:
    """Swap image axes
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "swap_axes")
    dst.data = np.transpose(src.data)
    src.remove_all_shapes()
    return dst


def compute_abs(src: ImageObj) -> ImageObj:
    """Compute absolute value
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "abs")
    dst.data = np.abs(src.data)
    return dst


def compute_re(src: ImageObj) -> ImageObj:
    """Compute real part
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "re")
    dst.data = np.real(src.data)
    return dst


def compute_im(src: ImageObj) -> ImageObj:
    """Compute imaginary part
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "im")
    dst.data = np.imag(src.data)
    return dst


class DataTypeIParam(gds.DataSet):
    """Convert image data type parameters"""

    dtype_str = gds.ChoiceItem(
        _("Destination data type"),
        list(zip(VALID_DTYPES_STRLIST, VALID_DTYPES_STRLIST)),
        help=_("Output image data type."),
    )


def compute_astype(src: ImageObj, p: DataTypeIParam) -> ImageObj:
    """Convert image data type
    Args:
        src: input image object
        p: parameters
    Returns:
        Output image object
    """
    dst = dst_11(src, "astype", p.dtype_str)
    dst.data = src.data.astype(p.dtype_str)
    return dst


def compute_log10(src: ImageObj) -> ImageObj:
    """Compute log10
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "log10")
    dst.data = np.log10(src.data)
    return dst


class ZCalibrateParam(gds.DataSet):
    """Image linear calibration parameters"""

    a = gds.FloatItem("a", default=1.0)
    b = gds.FloatItem("b", default=0.0)


def compute_calibration(src: ImageObj, p: ZCalibrateParam) -> ImageObj:
    """Compute linear calibration
    Args:
        src (ImageObj): input image object
        param (ZCalibrateParam): calibration parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "calibration", f"z={p.a}*z+{p.b}")
    dst.data = p.a * src.data + p.b
    return dst


def compute_threshold(src: ImageObj, p: ThresholdParam) -> ImageObj:
    """Apply thresholding
    Args:
        src (ImageObj): input image object
        p (ThresholdParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "threshold", f"min={p.value} lsb")
    dst.data = np.clip(src.data, p.value, src.data.max())
    return dst


def compute_clip(src: ImageObj, p: ClipParam) -> ImageObj:
    """Apply clipping
    Args:
        src (ImageObj): input image object
        p (ClipParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "clip", f"max={p.value} lsb")
    dst.data = np.clip(src.data, src.data.min(), p.value)
    return dst


def compute_gaussian_filter(src: ImageObj, p: GaussianParam) -> ImageObj:
    """Compute gaussian filter
    Args:
        src (ImageObj): input image object
        p (GaussianParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "gaussian_filter", f"σ={p.sigma:.3f} pixels")
    dst.data = spi.gaussian_filter(src.data, sigma=p.sigma)
    return dst


def compute_moving_average(src: ImageObj, p: MovingAverageParam) -> ImageObj:
    """Compute moving average
    Args:
        src (ImageObj): input image object
        p (MovingAverageParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "moving_average", f"n={p.n}")
    dst.data = spi.uniform_filter(src.data, size=p.n, mode="constant")
    return dst


def compute_moving_median(src: ImageObj, p: MovingMedianParam) -> ImageObj:
    """Compute moving median
    Args:
        src (ImageObj): input image object
        p (MovingMedianParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "moving_median", f"n={p.n}")
    dst.data = sps.medfilt(src.data, kernel_size=p.n)
    return dst


def compute_wiener(src: ImageObj) -> ImageObj:
    """Compute Wiener filter
    Args:
        src (ImageObj): input image object
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "wiener")
    dst.data = sps.wiener(src.data)
    return dst


def compute_fft(src: ImageObj, p: FFTParam) -> ImageObj:
    """Compute FFT
    Args:
        src (ImageObj): input image object
        p (FFTParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "fft")
    dst.data = z_fft(src.data, shift=p.shift)
    return dst


def compute_ifft(src: ImageObj, p: FFTParam) -> ImageObj:
    """Compute inverse FFT
    Args:
        src (ImageObj): input image object
        p (FFTParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "ifft")
    dst.data = z_ifft(src.data, shift=p.shift)
    return dst


class ButterworthParam(gds.DataSet):
    """Butterworth filter parameters"""

    cut_off = gds.FloatItem(
        _("Cut-off frequency ratio"),
        default=0.5,
        min=0.0,
        max=1.0,
        help=_("Cut-off frequency ratio (0.0 - 1.0)."),
    )
    high_pass = gds.BoolItem(
        _("High-pass filter"),
        default=False,
        help=_("If True, apply high-pass filter instead of low-pass."),
    )
    order = gds.IntItem(
        _("Order"),
        default=2,
        min=1,
        help=_("Order of the Butterworth filter."),
    )


def compute_butterworth(src: ImageObj, p: ButterworthParam) -> ImageObj:
    """Compute Butterworth filter
    Args:
        src (ImageObj): input image object
        p (ButterworthParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(
        src,
        "butterworth",
        f"cut_off={p.cut_off:.3f}, order={p.order}, high_pass={p.high_pass}",
    )
    dst.data = filters.butterworth(src.data, p.cut_off, p.high_pass, p.order)
    return dst


def calc_with_osr(image: ImageObj, func: Callable, *args: Any) -> np.ndarray:
    """Exec computation taking into account image x0, y0, dx, dy and ROIs"""
    res = []
    num_cols = []
    for i_roi in image.iterate_roi_indexes():
        data_roi = image.get_data(i_roi)
        if args is None:
            coords = func(data_roi)
        else:
            coords = func(data_roi, *args)
        if coords.size:
            if image.roi is not None:
                x0, y0, _x1, _y1 = RoiDataItem(image.roi[i_roi]).get_rect()
                coords[:, ::2] += x0
                coords[:, 1::2] += y0
            coords[:, ::2] = image.dx * coords[:, ::2] + image.x0
            coords[:, 1::2] = image.dy * coords[:, 1::2] + image.y0
            idx = np.ones((coords.shape[0], 1)) * i_roi
            coords = np.hstack([idx, coords])
            res.append(coords)
            num_cols.append(coords.shape[1])
    if res:
        if len(set(num_cols)) != 1:
            # This happens when the number of columns is not the same for all ROIs.
            # As of now, this happens only for polygon contours.
            # We need to pad the arrays with NaNs.
            max_cols = max(num_cols)
            num_rows = sum(coords.shape[0] for coords in res)
            out = np.full((num_rows, max_cols), np.nan)
            row = 0
            for coords in res:
                out[row : row + coords.shape[0], : coords.shape[1]] = coords
                row += coords.shape[0]
            return out
        return np.vstack(res)
    return None


def get_centroid_coords(data: np.ndarray) -> np.ndarray:
    """Return centroid coordinates
    Args:
        data (numpy.ndarray): input data
    Returns:
        np.ndarray: centroid coordinates
    """
    y, x = get_centroid_fourier(data)
    return np.array([(x, y)])


def compute_centroid(image: ImageObj) -> np.ndarray:
    """Compute centroid
    Args:
        image (ImageObj): input image
    Returns:
        np.ndarray: centroid coordinates
    """
    return calc_with_osr(image, get_centroid_coords)


def get_enclosing_circle_coords(data: np.ndarray) -> np.ndarray:
    """Return diameter coords for the circle contour enclosing image
    values above threshold (FWHM)
    Args:
        data (numpy.ndarray): input data
    Returns:
        np.ndarray: diameter coords
    """
    x, y, r = get_enclosing_circle(data)
    return np.array([[x - r, y, x + r, y]])


def compute_enclosing_circle(image: ImageObj) -> np.ndarray:
    """Compute minimum enclosing circle
    Args:
        image (ImageObj): input image
    Returns:
        np.ndarray: diameter coords
    """
    return calc_with_osr(image, get_enclosing_circle_coords)


class HoughCircleParam(gds.DataSet):
    """Circle Hough transform parameters"""

    min_radius = gds.IntItem(
        _("Radius<sub>min</sub>"), unit="pixels", min=0, nonzero=True
    )
    max_radius = gds.IntItem(
        _("Radius<sub>max</sub>"), unit="pixels", min=0, nonzero=True
    )
    min_distance = gds.IntItem(_("Minimal distance"), min=0)


def compute_hough_circle_peaks(image: ImageObj, p: HoughCircleParam) -> np.ndarray:
    """Compute Hough circles
    Args:
        image (ImageObj): input image
        p (HoughCircleParam): parameters
    Returns:
        np.ndarray: circle coordinates
    """
    return calc_with_osr(
        image,
        get_hough_circle_peaks,
        p.min_radius,
        p.max_radius,
        None,
        p.min_distance,
    )
