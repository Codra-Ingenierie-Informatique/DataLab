DataLab user guide
=======================

DataLab is a **generic signal and image processing software**.
It is based on Python scientific libraries (such as NumPy,
SciPy or scikit-image) and Qt graphical user interfaces
(thanks to `guidata`_ and `guiqwt`_ libraries).

.. figure:: images/DataLab-Overview.png

    Signal and image visualization in DataLab

DataLab features are available not only using the
**stand-alone application**
(easily installed thanks to the Windows installer or the Python package)
but also by **embedding it into your own application**
(see the "embedded tests" for detailed examples of how to do so).

External resources:
    .. list-table::
        :widths: 20, 80

        * - `Home`_
          - DataLab home page
        * - `PyPI`_
          - Python Package Index
        * - `GitHub`_
          - Bug reports and feature requests

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   overview
   roadmap
   features/general/index
   features/signal/index
   features/image/index

Copyrights and licensing
------------------------

- Copyright © 2023 `Codra`_, Pierre Raybaut
- Licensed under the terms of the `BSD 3-Clause`_

.. _guidata: https://pypi.python.org/pypi/guidata
.. _guiqwt: https://pypi.python.org/pypi/guiqwt
.. _PyPI: https://pypi.python.org/pypi/cdl
.. _Home: https://codra-ingenierie-informatique.github.io/DataLab/
.. _GitHub: https://github.com/Codra-Ingenierie-Informatique/DataLab
.. _Codra: https://codra.net/
.. _BSD 3-Clause: https://github.com/Codra-Ingenierie-Informatique/DataLab/blob/master/LICENSE
