# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Process isolation unit test
---------------------------

Just test if it's possible to run the process isolation test from another module. This
may be an issue with the Pool object being global.
"""

# guitest: show

from cdl.tests.backbone import procisolation1_unit


def test_procisolation():
    """Test process isolation"""
    procisolation1_unit.test()


if __name__ == "__main__":
    test_procisolation()
