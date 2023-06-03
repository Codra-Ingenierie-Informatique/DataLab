# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
DataLab unit tests
"""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager

from guidata.guitest import run_testlauncher

import cdl.config  # Loading icons
from cdl.core.gui.main import CDLMainWindow
from cdl.core.gui.panel.image import ImagePanel
from cdl.core.gui.panel.signal import SignalPanel
from cdl.env import execenv
from cdl.utils import qthelpers as qth
from cdl.utils import tests

# TODO: [P2] Documentation: add more screenshots from tests


@contextmanager
def cdl_app_context(
    size: tuple[int, int] = None,
    maximized: bool = False,
    save: bool = False,
    console: bool | None = None,
    exec_loop: bool = True,
) -> Generator[CDLMainWindow, None, None]:
    """Context manager handling DataLab mainwindow creation and Qt event loop"""
    if size is None:
        size = 950, 600

    # Enable test mode (e.g. raises exceptions during computations)
    execenv.test_mode = True

    with qth.qt_app_context(exec_loop=exec_loop):
        try:
            win = CDLMainWindow(console=console)
            if maximized:
                win.showMaximized()
            else:
                width, height = size
                win.resize(width, height)
                win.showNormal()
            win.show()
            win.setObjectName(tests.get_default_test_name())  # screenshot name
            yield win
        finally:
            if save:
                path = tests.get_output_data_path("h5")
                try:
                    os.remove(path)
                    win.save_to_h5_file(path)
                except PermissionError:
                    pass
            if not exec_loop:
                # Closing main window properly
                win.set_modified(False)
                win.close()


def take_plotwidget_screenshot(panel: SignalPanel | ImagePanel, name: str) -> None:
    """Eventually takes plotwidget screenshot (only in screenshot mode)"""
    if execenv.screenshot:
        prefix = panel.PARAMCLASS.PREFIX
        qth.grab_save_window(panel.plothandler.plotwidget, f"{prefix}_{name}")


def run() -> None:
    """Run DataLab test launcher"""
    run_testlauncher(cdl)


if __name__ == "__main__":
    run()
