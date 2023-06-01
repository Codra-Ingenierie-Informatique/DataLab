# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Restoration computation module
------------------------------

"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

# Note:
# ----
# All dataset classes must also be imported in the cdl.core.computation.param module.

from __future__ import annotations

import guidata.dataset.dataitems as gdi
import guidata.dataset.datatypes as gdt
import pywt
from skimage import morphology
from skimage.restoration import denoise_bilateral, denoise_tv_chambolle, denoise_wavelet

from cdl.config import _
from cdl.core.computation.image import dst_11
from cdl.core.computation.image.morphology import MorphologyParam
from cdl.core.model.image import ImageObj


class DenoiseTVParam(gdt.DataSet):
    """Total Variation denoising parameters"""

    weight = gdi.FloatItem(
        _("Denoising weight"),
        default=0.1,
        min=0,
        nonzero=True,
        help=_(
            "The greater weight, the more denoising "
            "(at the expense of fidelity to input)."
        ),
    )
    eps = gdi.FloatItem(
        "Epsilon",
        default=0.0002,
        min=0,
        nonzero=True,
        help=_(
            "Relative difference of the value of the cost function that "
            "determines the stop criterion. The algorithm stops when: "
            "(E_(n-1) - E_n) < eps * E_0"
        ),
    )
    max_num_iter = gdi.IntItem(
        _("Max. iterations"),
        default=200,
        min=0,
        nonzero=True,
        help=_("Maximal number of iterations used for the optimization"),
    )


def compute_denoise_tv(src: ImageObj, p: DenoiseTVParam) -> ImageObj:
    """Compute Total Variation denoising
    Args:
        src (ImageObj): input image object
        p (DenoiseTVParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(
        src,
        "denoise_tv",
        f"weight={p.weight}, eps={p.eps}, max_num_iter={p.max_num_iter}",
    )
    dst.data = denoise_tv_chambolle(
        src.data, weight=p.weight, eps=p.eps, max_num_iter=p.max_num_iter
    )
    return dst


class DenoiseBilateralParam(gdt.DataSet):
    """Bilateral filter denoising parameters"""

    sigma_spatial = gdi.FloatItem(
        "σ<sub>spatial</sub>",
        default=1.0,
        min=0,
        nonzero=True,
        unit="pixels",
        help=_(
            "Standard deviation for range distance. "
            "A larger value results in averaging of pixels "
            "with larger spatial differences."
        ),
    )
    _modelist = ("constant", "edge", "symmetric", "reflect", "wrap")
    mode = gdi.ChoiceItem(
        _("Mode"), list(zip(_modelist, _modelist)), default="constant"
    )
    cval = gdi.FloatItem(
        "cval",
        default=0,
        help=_(
            "Used in conjunction with mode 'constant', "
            "the value outside the image boundaries."
        ),
    )


def compute_denoise_bilateral(src: ImageObj, p: DenoiseBilateralParam) -> ImageObj:
    """Compute bilateral filter denoising
    Args:
        src (ImageObj): input image object
        p (DenoiseBilateralParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(
        src,
        "denoise_bilateral",
        f"σspatial={p.sigma_spatial}, mode={p.mode}, cval={p.cval}",
    )
    dst.data = denoise_bilateral(
        src.data,
        sigma_spatial=p.sigma_spatial,
        mode=p.mode,
        cval=p.cval,
    )
    return dst


class DenoiseWaveletParam(gdt.DataSet):
    """Wavelet denoising parameters"""

    _wavelist = pywt.wavelist()
    wavelet = gdi.ChoiceItem(
        _("Wavelet"), list(zip(_wavelist, _wavelist)), default="sym9"
    )
    _modelist = ("soft", "hard")
    mode = gdi.ChoiceItem(_("Mode"), list(zip(_modelist, _modelist)), default="soft")
    _methlist = ("BayesShrink", "VisuShrink")
    method = gdi.ChoiceItem(
        _("Method"), list(zip(_methlist, _methlist)), default="VisuShrink"
    )


def compute_denoise_wavelet(src: ImageObj, p: DenoiseWaveletParam) -> ImageObj:
    """Compute Wavelet denoising
    Args:
        src (ImageObj): input image object
        p (DenoiseWaveletParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(
        src,
        "denoise_wavelet",
        f"wavelet={p.wavelet}, mode={p.mode}, method={p.method}",
    )
    dst.data = denoise_wavelet(
        src.data,
        wavelet=p.wavelet,
        mode=p.mode,
        method=p.method,
    )
    return dst


def compute_denoise_tophat(src: ImageObj, p: MorphologyParam) -> ImageObj:
    """Denoise using White Top-Hat
    Args:
        src (ImageObj): input image object
        p (MorphologyParam): parameters
    Returns:
        ImageObj: output image object
    """
    dst = dst_11(src, "denoise_tophat", f"radius={p.radius}")
    dst.data = src.data - morphology.white_tophat(src.data, morphology.disk(p.radius))
    return dst
