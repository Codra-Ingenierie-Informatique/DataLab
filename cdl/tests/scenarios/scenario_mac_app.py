# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Macro-commands test scenario
----------------------------

Testing all the macro-commands features.
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import os.path as osp
import time

from cdl.core.gui.macroeditor import Macro
from cdl.core.gui.main import CDLMainWindow
from cdl.tests import cdl_app_context
from cdl.utils.tests import temporary_directory

SHOW = True  # Show test in GUI-based test launcher


def add_macro_sample(win: CDLMainWindow, index: int) -> Macro:
    """Add a macro sample to the macro panel

    Args:
        win: CDLMainWindow
        index: index of the macro sample to add
    """
    macro = win.macropanel.add_macro(f"Test macro {index}")
    samples = [
        "import time; [print(f'{i}:{time.sleep(.1)}') for i in range(50)]",
        "print('Hello world')",
    ]
    assert index < len(samples), f"index={index} is out of range"
    macro.set_code(samples[index])
    return macro


def test() -> None:
    """Example of high-level test scenario with HDF5 file"""
    with temporary_directory() as tmpdir:
        with cdl_app_context(console=False) as win:
            win.switch_to_panel("macro")
            add_macro_sample(win, 0)
            win.macropanel.run_macro()
            time.sleep(1)
            win.macropanel.stop_macro()
            code2 = add_macro_sample(win, 1).get_code()
            fname = osp.join(tmpdir, "test.macro")
            win.macropanel.export_macro_to_file(1, fname)
            win.macropanel.remove_macro()
            macro2 = win.macropanel.import_macro_from_file(fname)
            assert macro2.get_code() == code2, "Macro code is not the same"


if __name__ == "__main__":
    test()