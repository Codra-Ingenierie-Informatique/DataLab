# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Object model (:mod:`cdl.obj`)
-----------------------------

The :mod:`cdl.obj` module aims at providing all the necessary classes and functions
to create and manipulate DataLab signal and image objects.

Those classes and functions are defined in other modules:
    - :mod:`cdl.core.model.base`
    - :mod:`cdl.core.model.image`
    - :mod:`cdl.core.model.signal`
    - :mod:`cdl.core.io`

The :mod:`cdl.obj` module is thus a convenient way to import all the objects at once.
As a matter of fact, the following import statement is equivalent to the previous one:

.. code-block:: python

    # Original import statement
    from cdl.core.model.signal import SignalObj
    from cdl.core.model.image import ImageObj

    # Equivalent import statement
    from cdl.obj import SignalObj, ImageObj

Common objects
^^^^^^^^^^^^^^

.. autoclass:: cdl.obj.ResultShape
    :members:
.. autoclass:: cdl.obj.ShapeTypes
    :members:
.. autoclass:: cdl.obj.UniformRandomParam
.. autoclass:: cdl.obj.NormalRandomParam

Signal model
^^^^^^^^^^^^

.. autoclass:: cdl.obj.SignalObj
    :members:
    :inherited-members:
.. autofunction:: cdl.obj.read_signal
.. autofunction:: cdl.obj.create_signal
.. autofunction:: cdl.obj.create_signal_from_param
.. autofunction:: cdl.obj.new_signal_param
.. autoclass:: cdl.obj.SignalTypes
.. autoclass:: cdl.obj.NewSignalParam
.. autoclass:: cdl.obj.GaussLorentzVoigtParam
.. autoclass:: cdl.obj.StepParam
.. autoclass:: cdl.obj.PeriodicParam

Image model
^^^^^^^^^^^

.. autoclass:: cdl.obj.ImageObj
    :members:
    :inherited-members:
.. autofunction:: cdl.obj.read_image
.. autofunction:: cdl.obj.create_image
.. autofunction:: cdl.obj.create_image_from_param
.. autofunction:: cdl.obj.new_image_param
.. autoclass:: cdl.obj.ImageTypes
.. autoclass:: cdl.obj.NewImageParam
.. autoclass:: cdl.obj.Gauss2DParam
.. autoclass:: cdl.obj.RoiDataGeometries
.. autoclass:: cdl.obj.ImageDatatypes
"""

# pylint:disable=unused-import
# flake8: noqa

from cdl.core.io import read_image, read_signal
from cdl.core.model.base import (
    NormalRandomParam,
    ResultShape,
    ShapeTypes,
    UniformRandomParam,
)
from cdl.core.model.image import (
    Gauss2DParam,
    ImageDatatypes,
    ImageObj,
    ImageTypes,
    NewImageParam,
    RoiDataGeometries,
    create_image,
    create_image_from_param,
    new_image_param,
)
from cdl.core.model.signal import (
    GaussLorentzVoigtParam,
    NewSignalParam,
    PeriodicParam,
    SignalObj,
    SignalTypes,
    StepParam,
    create_signal,
    create_signal_from_param,
    new_signal_param,
)
