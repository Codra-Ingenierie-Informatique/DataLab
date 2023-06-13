# -*- coding: utf-8 -*-
#
# Licensed under the terms of the BSD 3-Clause
# (see cdl/LICENSE for details)

"""
DataLab base proxy module
-------------------------
"""

from __future__ import annotations

import abc
from collections.abc import Callable
from typing import TYPE_CHECKING

import guidata.dataset.datatypes as gdt
import numpy as np

from cdl.obj import ImageObj, SignalObj

if TYPE_CHECKING:
    from cdl.core.gui.main import CDLMainWindow
    from cdl.core.remote import ServerProxy


class AbstractCDLControl(abc.ABC):
    """Abstract base class for controlling DataLab (main window or remote server)"""

    @abc.abstractmethod
    def get_version(self) -> str:
        """Return DataLab version.

        Returns:
            str: DataLab version
        """

    @abc.abstractmethod
    def close_application(self) -> None:
        """Close DataLab application"""

    @abc.abstractmethod
    def switch_to_panel(self, panel: str) -> None:
        """Switch to panel.

        Args:
            panel (str): Panel name (valid values: "signal", "image", "macro"))
        """

    @abc.abstractmethod
    def reset_all(self) -> None:
        """Reset all application data"""

    @abc.abstractmethod
    def save_to_h5_file(self, filename: str) -> None:
        """Save to a DataLab HDF5 file.

        Args:
            filename (str): HDF5 file name
        """

    @abc.abstractmethod
    def open_h5_files(
        self,
        h5files: list[str] | None = None,
        import_all: bool | None = None,
        reset_all: bool | None = None,
    ) -> None:
        """Open a DataLab HDF5 file or import from any other HDF5 file.

        Args:
            h5files (list[str], optional): List of HDF5 files to open. Defaults to None.
            import_all (bool, optional): Import all objects from HDF5 files.
                Defaults to None.
            reset_all (bool, optional): Reset all application data. Defaults to None.
        """

    @abc.abstractmethod
    def import_h5_file(self, filename: str, reset_all: bool | None = None) -> None:
        """Open DataLab HDF5 browser to Import HDF5 file.

        Args:
            filename (str): HDF5 file name
            reset_all (bool, optional): Reset all application data. Defaults to None.
        """

    @abc.abstractmethod
    def open_object(self, filename: str) -> None:
        """Open object from file in current panel (signal/image).

        Args:
            filename (str): File name
        """

    @abc.abstractmethod
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

        # TODO: Check if this is really needed: data type is already checked in
        # "add_object" method of "CDLMainWindow" class
        # dtypes = SignalObj.VALID_DTYPES
        # dtnames = ", ".join([dtype.__name__ for dtype in dtypes])
        # if xdata.dtype not in dtypes:
        #     raise ValueError(
        #         f"xdata dtype must be one of {dtnames}, got {xdata.dtype.name}"
        #     )
        # if ydata.dtype not in dtypes:
        #     raise ValueError(
        #         f"ydata dtype must be one of {dtnames}, got {ydata.dtype.name}"
        #     )

    @abc.abstractmethod
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

    def add_object(self, obj: SignalObj | ImageObj) -> None:
        """Add object to DataLab.

        Args:
            obj (SignalObj | ImageObj): Signal or image object
        """
        if isinstance(obj, SignalObj):
            self.add_signal(
                obj.title, obj.x, obj.y, obj.xunit, obj.yunit, obj.xlabel, obj.ylabel
            )
        elif isinstance(obj, ImageObj):
            self.add_image(
                obj.title,
                obj.data,
                obj.xunit,
                obj.yunit,
                obj.zunit,
                obj.xlabel,
                obj.ylabel,
                obj.zlabel,
            )

    @abc.abstractmethod
    def get_object_titles(self, panel: str | None = None) -> list[str]:
        """Get object (signal/image) list for current panel

        Args:
            panel (str | None): panel name (valid values: "signal", "image").
                If None, current panel is used.

        Returns:
            list[str]: list of object titles

        Raises:
            ValueError: if panel not found
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
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

    @abc.abstractmethod
    def get_object_uuids(self, panel: str | None = None) -> list[str]:
        """Get object (signal/image) uuid list for current panel

        Args:
            panel (str | None): panel name (valid values: "signal", "image").
                If None, current panel is used.

        Returns:
            list[str]: list of object uuids

        Raises:
            ValueError: if panel not found
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def calc(self, name: str, param: gdt.DataSet | None = None) -> gdt.DataSet:
        """Call compute function ``name`` in current panel's processor.

        Args:
            name (str): Compute function name
            param (gdt.DataSet, optional): Compute function parameter. Defaults to None.

        Returns:
            gdt.DataSet: Compute function result
        """

    def __getattr__(self, name: str) -> Callable:
        """Return compute function ``name`` in current panel's processor.

        Args:
            name (str): Compute function name

        Returns:
            Callable: Compute function

        Raises:
            AttributeError: If compute function ``name`` does not exist
        """

        def compute_func(param: gdt.DataSet | None = None) -> gdt.DataSet:
            """Compute function.

            Args:
                param (gdt.DataSet, optional): Compute function parameter.
                    Defaults to None.

            Returns:
                gdt.DataSet: Compute function result
            """
            return self.calc(name, param)

        if name.startswith("compute_"):
            return compute_func
        raise AttributeError(f"DataLab has no compute function '{name}'")


class BaseProxy(AbstractCDLControl, metaclass=abc.ABCMeta):
    """Common base class for DataLab proxies"""

    def __init__(self, cdl: CDLMainWindow | ServerProxy | None = None) -> None:
        self._cdl = cdl

    def get_version(self) -> str:
        """Return DataLab version.

        Returns:
            str: DataLab version
        """
        return self._cdl.get_version()

    def close_application(self) -> None:
        """Close DataLab application"""
        self._cdl.close_application()

    def switch_to_panel(self, panel: str) -> None:
        """Switch to panel.

        Args:
            panel (str): Panel name (valid values: "signal", "image", "macro"))
        """
        self._cdl.switch_to_panel(panel)

    def reset_all(self) -> None:
        """Reset all application data"""
        self._cdl.reset_all()

    def save_to_h5_file(self, filename: str) -> None:
        """Save to a DataLab HDF5 file.

        Args:
            filename (str): HDF5 file name
        """
        self._cdl.save_to_h5_file(filename)

    def open_h5_files(
        self,
        h5files: list[str] | None = None,
        import_all: bool | None = None,
        reset_all: bool | None = None,
    ) -> None:
        """Open a DataLab HDF5 file or import from any other HDF5 file.

        Args:
            h5files (list[str], optional): List of HDF5 files to open. Defaults to None.
            import_all (bool, optional): Import all objects from HDF5 files.
                Defaults to None.
            reset_all (bool, optional): Reset all application data. Defaults to None.
        """
        self._cdl.open_h5_files(h5files, import_all, reset_all)

    def import_h5_file(self, filename: str, reset_all: bool | None = None) -> None:
        """Open DataLab HDF5 browser to Import HDF5 file.

        Args:
            filename (str): HDF5 file name
            reset_all (bool, optional): Reset all application data. Defaults to None.
        """
        self._cdl.import_h5_file(filename, reset_all)

    def open_object(self, filename: str) -> None:
        """Open object from file in current panel (signal/image).

        Args:
            filename (str): File name
        """
        self._cdl.open_object(filename)

    def get_object_titles(self, panel: str | None = None) -> list[str]:
        """Get object (signal/image) list for current panel

        Args:
            panel (str | None): panel name (valid values: "signal", "image").
                If None, current panel is used.

        Returns:
            list[str]: list of object titles

        Raises:
            ValueError: if panel not found
        """
        return self._cdl.get_object_titles(panel)

    def get_object_uuids(self, panel: str | None = None) -> list[str]:
        """Get object (signal/image) uuid list for current panel

        Args:
            panel (str | None): panel name (valid values: "signal", "image").
                If None, current panel is used.

        Returns:
            list[str]: list of object uuids

        Raises:
            ValueError: if panel not found
        """
        return self._cdl.get_object_uuids(panel)
