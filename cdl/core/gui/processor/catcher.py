# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
DataLab warning and error catcher utility for processors
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from __future__ import annotations

import dataclasses
import traceback
import warnings
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from cdl.env import execenv

if TYPE_CHECKING:  # pragma: no cover
    import numpy as np

    from cdl.core.model.image import ImageObj
    from cdl.core.model.signal import SignalObj


@dataclasses.dataclass
class CompOut:
    """Class for representing computation output
    Attributes:
        result (SignalObj | ImageObj | np.ndarray | None): computation result
        error_msg (str | None): error message
        warning_msg (str | None): warning message
    """

    result: SignalObj | ImageObj | np.ndarray | None = None
    error_msg: str | None = None
    warning_msg: str | None = None


def wng_err_func(func: Callable, args: tuple[Any]) -> CompOut:
    """Wrapper function to catch errors and warnings during computation
    Args:
        func (Callable): function to call
        args (tuple[Any]): function arguments
    Returns:
        CompOut: computation output
    """
    with warnings.catch_warnings(record=True) as wngs:
        try:
            result = func(*args)
            if wngs:
                wng = wngs[-1]
                warning_msg = warnings.formatwarning(
                    message=wng.message,
                    category=wng.category,
                    filename=wng.filename,
                    lineno=wng.lineno,
                    line=wng.line,
                )
                return CompOut(result=result, warning_msg=warning_msg)
            return CompOut(result=result)
        except Exception:  # pylint: disable=broad-except
            if execenv.test_mode:
                #  In test mode, we want to raise the exception because test cases
                #  are supposed to work without any error. In real life, we want to
                #  avoid raising the exception because it would stop the application,
                #  and exceptions could be related to non-critical errors due to
                #  external libraries.
                raise
            return CompOut(error_msg=traceback.format_exc())