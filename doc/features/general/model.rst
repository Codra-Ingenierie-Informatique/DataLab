.. _ref-to-model:

Internal data model
===================

In its internal data model, DataLab stores data using two main classes:

* `cdl.core.model.signal.SignalObj`, which represents a signal object, and
* `cdl.core.model.image.ImageObj`, which represents an image object.

These classes are defined in the `cdl.core.model` package but are exposed
publicly in the `cdl.obj` package.

Also, DataLab uses many different datasets (based on guidata's `DataSet` class)
to store the parameters of the computations. These datasets are defined in
different modules but are exposed publicly in the `cdl.param` package.

.. seealso::

    The :ref:`api` section for more information on the public API.
