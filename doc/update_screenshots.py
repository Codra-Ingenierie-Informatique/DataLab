# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Module for taking DataLab screenshots
"""

from cdl import config
from cdl.tests.scenarios import beautiful_app

if __name__ == "__main__":
    print("Updating screenshots...", end=" ")
    config.reset()  # Reset configuration (remove configuration file and initialize it)
    beautiful_app.run_beautiful_scenario(screenshots=True)
    print("done.")
