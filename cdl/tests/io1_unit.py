# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
I/O test

Testing DataLab specific formats.
"""

from cdl.core.io import read_signal
from cdl.core.io.image import funcs as image_funcs
from cdl.env import execenv
from cdl.utils.qthelpers import qt_app_context
from cdl.utils.tests import try_open_test_data
from cdl.utils.vistools import view_curve_items, view_images

SHOW = True  # Show test in GUI-based test launcher


@try_open_test_data("Testing CSV file reader", "*.txt")
def test_csv(fname=None):
    """Testing CSV files"""
    signal = read_signal(fname)
    execenv.print(signal)
    view_curve_items([signal.make_item()])


@try_open_test_data("Testing SIF file handler", "*.sif")
def test_sif(fname=None):
    """Testing SIF files"""
    execenv.print(image_funcs.SIFFile(fname))
    data = image_funcs.imread_sif(fname)[0]
    view_images(data)


@try_open_test_data("Testing FXD file handler", "*.fxd")
def test_fxd(fname=None):
    """Testing FXD files"""
    execenv.print(image_funcs.FXDFile(fname))
    data = image_funcs.imread_fxd(fname)
    view_images(data)


@try_open_test_data("Testing SCOR-DATA file handler", "*.scor-data")
def test_scordata(fname=None):
    """Testing SCOR-DATA files"""
    execenv.print(image_funcs.SCORFile(fname))
    data = image_funcs.imread_scor(fname)
    view_images(data)


def io_test():
    """I/O test"""
    with qt_app_context():
        test_csv()
        test_sif()
        test_fxd()
        test_scordata()


if __name__ == "__main__":
    io_test()
