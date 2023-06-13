# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
DataLab proxy module
--------------------

This module provides a way to access DataLab features from a proxy class.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

import guidata.dataset.datatypes as gdt
import numpy as np

from cdl.core.baseproxy import BaseProxy
from cdl.core.remote import RemoteClient
from cdl.obj import ImageObj, SignalObj
from cdl.utils import qthelpers as qth


class RemoteCDLProxy(RemoteClient):
    """DataLab proxy class.

    This class provides access to DataLab features from a proxy class.
    """

    def __init__(self, port: str | None = None):
        super().__init__()
        self.connect(port)


class CDLProxy(BaseProxy):
    """DataLab proxy class.

    This class provides access to DataLab features from a proxy class.
    """

    def add_signal(
        self,
        title: str,
        xdata: np.ndarray,
        ydata: np.ndarray,
        xunit: str | None = None,
        yunit: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
    ) -> bool:  # pylint: disable=too-many-arguments
        """Add signal data to DataLab.

        Args:
            title (str): Signal title
            xdata (np.ndarray): X data
            ydata (np.ndarray): Y data
            xunit (str, optional): X unit. Defaults to None.
            yunit (str, optional): Y unit. Defaults to None.
            xlabel (str, optional): X label. Defaults to None.
            ylabel (str, optional): Y label. Defaults to None.

        Returns:
            bool: True if signal was added successfully, False otherwise

        Raises:
            ValueError: Invalid xdata dtype
            ValueError: Invalid ydata dtype
        """
        return self._cdl.add_signal(title, xdata, ydata, xunit, yunit, xlabel, ylabel)

    def add_image(
        self,
        title: str,
        data: np.ndarray,
        xunit: str | None = None,
        yunit: str | None = None,
        zunit: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        zlabel: str | None = None,
    ) -> bool:  # pylint: disable=too-many-arguments
        """Add image data to DataLab.

        Args:
            title (str): Image title
            data (np.ndarray): Image data
            xunit (str, optional): X unit. Defaults to None.
            yunit (str, optional): Y unit. Defaults to None.
            zunit (str, optional): Z unit. Defaults to None.
            xlabel (str, optional): X label. Defaults to None.
            ylabel (str, optional): Y label. Defaults to None.
            zlabel (str, optional): Z label. Defaults to None.

        Returns:
            bool: True if image was added successfully, False otherwise

        Raises:
            ValueError: Invalid data dtype
        """
        return self._cdl.add_image(
            title, data, xunit, yunit, zunit, xlabel, ylabel, zlabel
        )

    def calc(self, name: str, param: gdt.DataSet | None = None) -> gdt.DataSet:
        """Call compute function ``name`` in current panel's processor.

        Args:
            name (str): Compute function name
            param (gdt.DataSet, optional): Compute function parameter. Defaults to None.

        Returns:
            gdt.DataSet: Compute function result
        """
        return self._cdl.calc(name, param)

    def get_object_from_title(
        self, title: str, panel: str | None = None
    ) -> SignalObj | ImageObj:
        """Get object (signal/image) from title

        Args:
            title (str): object
            panel (str | None): panel name (valid values: "signal", "image").
                If None, current panel is used.

        Returns:
            Union[SignalObj, ImageObj]: object

        Raises:
            ValueError: if object not found
            ValueError: if panel not found
        """
        return self._cdl.get_object_from_title(title, panel)

    def get_object(
        self,
        index: int | None = None,
        group_index: int | None = None,
        panel: str | None = None,
    ) -> SignalObj | ImageObj:
        """Get object (signal/image) from index.

        Args:
            index (int): Object index in current panel. Defaults to None.
            group_index (int, optional): Group index. Defaults to None.
            panel (str, optional): Panel name. Defaults to None.

        If ``index`` is not specified, returns the currently selected object.
        If ``group_index`` is not specified, return an object from the current group.
        If ``panel`` is not specified, return an object from the current panel.

        Returns:
            Union[SignalObj, ImageObj]: object

        Raises:
            IndexError: if object not found
        """
        return self._cdl.get_object(index, group_index, panel)

    def get_object_from_uuid(
        self, oid: str, panel: str | None = None
    ) -> SignalObj | ImageObj:
        """Get object (signal/image) from uuid

        Args:
            oid (str): object uuid
            panel (str | None): panel name (valid values: "signal", "image").

        Returns:
            Union[SignalObj, ImageObj]: object

        Raises:
            ValueError: if object not found
            ValueError: if panel not found
        """
        return self._cdl.get_object_from_uuid(oid, panel)


@contextmanager
def proxy_context(what: str) -> Generator[CDLProxy | RemoteCDLProxy, None, None]:
    """Context manager handling CDL proxy creation and destruction.

    Args:
        what (str): proxy type ("gui" or "remote")
            For remote proxy, the port can be specified as "remote:port"

    Yields:
        Generator[CDLProxy | RemoteCDLProxy, None, None]: proxy
            CDLProxy if what == "gui"
            RemoteCDLProxy if what == "remote" or "remote:port"
    """
    assert what == "gui" or what.startswith("remote"), "Invalid proxy type"
    xmlrpcport = None
    if ":" in what:
        xmlrpcport = int(what.split(":")[1].strip())
    if what == "gui":
        # pylint: disable=import-outside-toplevel
        from cdl.core.gui.main import CDLMainWindow

        with qth.qt_app_context(exec_loop=True):
            try:
                win = CDLMainWindow()
                proxy = CDLProxy(win)
                win.show()
                yield proxy
            finally:
                pass
    else:
        try:
            proxy = RemoteCDLProxy(xmlrpcport)
            yield proxy
        finally:
            proxy.disconnect()
