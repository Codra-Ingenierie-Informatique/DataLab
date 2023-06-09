# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
Test Data Plugin for DataLab
----------------------------

This plugin is an example of DataLab plugin. It provides test data samples
and some actions to test DataLab functionalities.
"""

import cdl.tests.data as test_data
from cdl.config import _
from cdl.core.computation import image as cpima
from cdl.core.computation import signal as cpsig
from cdl.obj import ImageObj, NormalRandomParam, SignalObj
from cdl.plugins import PluginBase, PluginInfo

# ------------------------------------------------------------------------------
# All computation functions must be defined as global functions, otherwise
# they cannot be pickled and sent to the worker process
# ------------------------------------------------------------------------------


def add_noise_to_signal(src: SignalObj, p: test_data.GaussianNoiseParam) -> SignalObj:
    """Add gaussian noise to signal"""
    dst = cpsig.dst_11(src, "add_gaussian_noise", f"mu={p.mu},sigma={p.sigma}")
    test_data.add_gaussian_noise_to_signal(dst, p)
    return dst


def add_noise_to_image(src: ImageObj, p: NormalRandomParam) -> ImageObj:
    """Add gaussian noise to image"""
    dst = cpima.dst_11(src, "add_gaussian_noise", f"mu={p.mu},sigma={p.sigma}")
    test_data.add_gaussian_noise_to_image(dst, p)
    return dst


class PluginTestData(PluginBase):
    """DataLab Test Data Plugin"""

    PLUGIN_INFO = PluginInfo(
        name=_("Test data"),
        version="1.0.0",
        description=_("Testing DataLab functionalities"),
    )

    # Signal processing features ------------------------------------------------
    def add_noise_to_signal(self) -> None:
        """Add noise to signal"""
        self.signalpanel.processor.compute_11(
            add_noise_to_signal,
            paramclass=test_data.GaussianNoiseParam,
            title=_("Add noise"),
        )

    def create_paracetamol_signal(self) -> None:
        """Create paracetamol signal"""
        panel = self.signalpanel
        obj = test_data.create_paracetamol_signal()
        panel.add_object(obj)

    def create_noisy_signal(self) -> None:
        """Create noisy signal"""
        panel = self.signalpanel
        obj = test_data.create_noisy_signal()
        panel.add_object(obj)

    # Image processing features ------------------------------------------------
    def add_noise_to_image(self) -> None:
        """Add noise to image"""
        self.imagepanel.processor.compute_11(
            add_noise_to_image,
            paramclass=NormalRandomParam,
            title=_("Add noise"),
        )

    def create_peak2d_image(self) -> None:
        """Create 2D peak image"""
        panel = self.imagepanel
        obj = test_data.create_peak2d_image()
        panel.add_object(obj)

    def create_sincos_image(self) -> None:
        """Create 2D sin cos image"""
        panel = self.imagepanel
        obj = test_data.create_sincos_image()
        panel.add_object(obj)

    def create_noisygauss_image(self) -> None:
        """Create 2D noisy gauss image"""
        panel = self.imagepanel
        obj = test_data.create_noisygauss_image()
        panel.add_object(obj)

    def create_multigauss_image(self) -> None:
        """Create 2D multi gauss image"""
        panel = self.imagepanel
        obj = test_data.create_multigauss_image()
        panel.add_object(obj)

    def create_2dstep_image(self) -> None:
        """Create 2D step image"""
        panel = self.imagepanel
        obj = test_data.create_2dstep_image()
        panel.add_object(obj)

    def create_annotated_image(self) -> None:
        """Create annotated image"""
        panel = self.imagepanel
        obj = test_data.create_annotated_image()
        panel.add_object(obj)

    # Plugin menu entries ------------------------------------------------------
    def create_actions(self) -> None:
        """Create actions"""
        # Signal panel ----------------------------------------------------------
        sah = self.signalpanel.acthandler
        with sah.new_menu(_("Test data")):
            sah.new_action(_("Add noise to signal"), triggered=self.add_noise_to_signal)
            sah.new_action(
                _("Load spectrum of paracetamol"),
                triggered=self.create_paracetamol_signal,
                select_condition="always",
                separator=True,
            )
            sah.new_action(
                _("Create noisy signal"),
                triggered=self.create_noisy_signal,
                select_condition="always",
            )
        # Image panel -----------------------------------------------------------
        iah = self.imagepanel.acthandler
        with iah.new_menu(_("Test data")):
            iah.new_action(_("Add noise to image"), triggered=self.add_noise_to_image)
            # with iah.new_menu(_("Data samples")):
            iah.new_action(
                _("Create image with peaks"),
                triggered=self.create_peak2d_image,
                select_condition="always",
                separator=True,
            )
            iah.new_action(
                _("Create 2D sin cos image"),
                triggered=self.create_sincos_image,
                select_condition="always",
            )
            iah.new_action(
                _("Create 2D noisy gauss image"),
                triggered=self.create_noisygauss_image,
                select_condition="always",
            )
            iah.new_action(
                _("Create 2D multi gauss image"),
                triggered=self.create_multigauss_image,
                select_condition="always",
            )
            iah.new_action(
                _("Create annotated image"),
                triggered=self.create_annotated_image,
                select_condition="always",
            )
            iah.new_action(
                _("Create 2D step image"),
                triggered=self.create_2dstep_image,
                select_condition="always",
            )