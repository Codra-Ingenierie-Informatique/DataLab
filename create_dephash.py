# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Create dependencies hash
"""

from cdl.config import DATAPATH
from cdl.utils import dephash

dephash.create_dependencies_file(DATAPATH, ("guidata", "plotpy"))
