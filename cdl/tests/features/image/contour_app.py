# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Contour finding application test
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...
# guitest: show

import cdl.obj
import cdl.param
from cdl.tests import cdl_app_context, take_plotwidget_screenshot
from cdl.tests.data import create_multigauss_image
from cdl.tests.features.common.roi_app import create_test_image_with_roi


def test():
    """Run contour finding application test scenario"""
    newparam = cdl.obj.new_image_param(height=200, width=200)
    with cdl_app_context() as win:
        panel = win.imagepanel
        ima1 = create_multigauss_image(newparam)
        panel.add_object(ima1)
        param = cdl.param.ContourShapeParam()
        panel.processor.compute_contour_shape(param)
        take_plotwidget_screenshot(panel, "contour_test")
        ima2 = create_test_image_with_roi(newparam)
        panel.add_object(ima2)
        panel.processor.edit_regions_of_interest()
        panel.processor.compute_contour_shape(param)


if __name__ == "__main__":
    test()
