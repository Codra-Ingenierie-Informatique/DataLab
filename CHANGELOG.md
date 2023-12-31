# Changelog #

See DataLab [roadmap page](https://cdlapp.readthedocs.io/en/latest/dev/roadmap.html)
for future and past milestones.

## DataLab Version 0.11.0 ##

💥 New features:

* Signals and images may now be reordered in the tree view:
  * Using the new "Move up" and "Move down" actions in the "Edit" menu (or using the
    corresponding toolbar buttons):
  * This fixes [Issue #22](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/22) - Add "move up/down" actions in "Edit" menu, for signals/images and groups
* Signals and images may also be reordered using drag and drop:
  * Signals and images can be dragged and dropped inside their own panel to change
    their order
  * Groups can also be dragged and dropped inside their panel
  * The feature also supports multi-selection (using the standard Ctrl and Shift
    modifiers), so that multiple signals/images/groups can be moved at once, not
    necessarily with contiguous positions
  * This fixes [Issue #17](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/17) - Add Drag and Drop feature to Signals/Images tree views
* New 1D interpolation features:
  * Added "Interpolation" feature to signal panel's "Processing" menu
  * Methods available: linear, spline, quadratic, cubic, barycentric and PCHIP
  * Thanks to @marcel-goldschen-ohm for the contribution to spline interpolation
  * This fixes [Issue #20](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/20) - Add 1D interpolation features
* New 1D resampling feature:
  * Added "Resampling" feature to signal panel's "Processing" menu
  * Same interpolation methods as for the "Interpolation" feature
  * Possibility to specify the resampling step or the number of points
  * This fixes [Issue #21](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/21) - Add 1D resampling feature
* New 1D convolution feature:
  * Added "Convolution" feature to signal panel's "Operation" menu
  * This fixes [Issue #23](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/23) - Add 1D convolution feature
* New 1D detrending feature:
  * Added "Detrending" feature to signal panel's "Processing" menu
  * Methods available: linear or constant
  * This fixes [Issue #24](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/24) - Add 1D detrending feature
* Increased default width of the object selection dialog box:
  * The object selection dialog box is now wider by default, so that the full
    signal/image/group titles may be more easily readable
* Automated test suite:
  * Since version 0.10, DataLab's proxy object has a `toggle_auto_refresh` method
    to toggle the "Auto-refresh" feature. This feature may be useful to improve
    performance during the execution of test scripts
  * Test scenarios on signals and images are now using this feature to improve
    performance

📚 Documentation:

* New [API section](https://cdlapp.readthedocs.io/en/latest/api/index.html) in the documentation:
  * This section explains how to use DataLab as a Python library, by covering the
  following topics:
    * How to use DataLab algorithms on NumPy arrays
    * How to use DataLab computation features on DataLab objects (signals and images)
    * How to use DataLab I/O features
    * How to use proxy objects to control DataLab remotely
  * This section also provides a complete API reference for DataLab objects and
  features
  * This fixes [Issue #19](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/19) - Add API documentation (data model, functions on arrays or signal/image objects, ...)

## DataLab Version 0.10.1 ##

*Note*: V0.10.0 was almost immediately replaced by V0.10.1 due to a last minute
bug fix

💥 New features:

* Features common to signals and images:
  * Added "Real part" and "Imaginary part" features to "Operation" menu
  * Added "Convert data type" feature to "Operation" menu
* Features added following user requests (12/18/2023 meetup @ CEA):
  * Curve and image styles are now saved in the HDF5 file:
    * Curve style covers the following properties: color, line style, line width,
      marker style, marker size, marker edge color, marker face color, etc.
    * Image style covers the following properties: colormap, interpolation, etc.
    * Those properties were already persistent during the working session, but
      were lost when saving and reloading the HDF5 file
    * Now, those properties are saved in the HDF5 file and are restored when
      reloading the HDF5 file
  * New profile extraction features for images:
    * Added "Extract profile" to "Operations" menu, to extract a profile from
      an image along a row or a column
    * Added "Extract average profile" to "Operations" menu, to extract the
      average profile on a rectangular area of an image, along a row or a column
  * Image LUT range (contrast/brightness settings) is now saved in the HDF5 file:
    * As for curve and image styles, the LUT range was already persistent during
      the working session, but was lost when saving and reloading the HDF5 file
    * Now, the LUT range is saved in the HDF5 file and is restored when reloading it
  * Added "Auto-refresh" and "Refresh manually" actions in "View" menu
    (and main toolbar):
    * When "Auto-refresh" is enabled (default), the plot view is automatically refreshed
      when a signal/image is modified, added or removed. Even though the refresh is
      optimized, this may lead to performance issues when working with large
      datasets.
    * When disabled, the plot view is not automatically refreshed. The user
      must manually refresh the plot view by clicking on the "Refresh manually" button
      in the main toolbar or by pressing the standard refresh key (e.g. "F5").
  * Added `toggle_auto_refresh` method to DataLab proxy object:
    * This method allows to toggle the "Auto-refresh" feature from a macro-command,
      a plugin or a remote control client.
    * A context manager `context_no_refresh` is also available to temporarily disable
      the "Auto-refresh" feature from a macro-command, a plugin or a remote control
      client. Typical usage:

      ```python
      with proxy.context_no_refresh():
          # Do something without refreshing the plot view
          proxy.compute_fft() # (...)
      ```

  * Improved curve readability:
    * Until this release, the curve style was automatically set by cycling through
      **PlotPy** predefined styles
    * However, some styles are not suitable for curve readability (e.g. "cyan" and
      "yellow" colors are not readable on a white background, especially when combined
      with a "dashed" line style)
    * This release introduces a new curve style management with colors which are
      distinguishable and accessible, even to color vision deficiency people
* Added "Curve anti-aliasing" feature to "View" menu (and toolbar):
  * This feature allows to enable/disable curve anti-aliasing (default: enabled)
  * When enabled, the curve rendering is smoother but may lead to performance issues
    when working with large datasets (that's why it can be disabled)
* Added `toggle_show_titles` method to DataLab proxy object. This method allows to
  toggle the "Show graphical object titles" feature from a macro-command, a plugin
  or a remote control client.
* Remote client is now checking the server version and shows a warning message if
  the server version may not be fully compatible with the client version.

🛠️ Bug fixes:

* Image contour detection feature ("Computing" menu):
  * The contour detection feature was not taking into account the "shape" parameter
    (circle, ellipse, polygon) when computing the contours. The parameter was stored
    but really used only when calling the feature a second time.
  * This unintentional behavior led to an `AssertionError` when choosing "polygon"
    as the contour shape and trying to compute the contours for the first time.
  * This is now fixed (see [Issue #9](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/9) - Image contour detection: `AssertionError` when choosing "polygon" as the contour shape)
* Keyboard shortcuts:
  * The keyboard shortcuts for "New", "Open", "Save", "Duplicate", "Remove",
    "Delete all" and "Refresh manually" actions were not working properly.
  * Those shortcuts were specific to each signal/image panel, and were working only
    when the panel on which the shortcut was pressed for the first time was active
    (when activated from another panel, the shortcut was not working and a warning
    message was displayed in the console,
    e.g. `QAction::event: Ambiguous shortcut overload: Ctrl+C`)
  * Besides, the shortcuts were not working at startup (when no panel had focus).
  * This is now fixed: the shortcuts are now working whatever the active panel is,
    and even at startup (see [Issue #10](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/10) - Keyboard shortcuts not working properly: `QAction::event: Ambiguous shortcut overload: Ctrl+C`)
* "Show graphical object titles" and "Auto-refresh" actions were not working properly:
  * The "Show graphical object titles" and "Auto-refresh" actions were only working on
    the active signal/image panel, and not on all panels.
  * This is now fixed (see [Issue #11](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/11) - "Show graphical object titles" and "Auto-refresh" actions were working only on current signal/image panel)
* Fixed [Issue #14](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/14) - Saving/Reopening HDF5 project without cleaning-up leads to `ValueError`
* Fixed [Issue #15](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/15) - MacOS: 1. `pip install cdl` error - 2. Missing menus:
  * Part 1: `pip install cdl` error on MacOS was actually an issue from **PlotPy** (see
    [this issue](https://github.com/PlotPyStack/PlotPy/issues/9)), and has been fixed
    in PlotPy v2.0.3 with an additional compilation flag indicating to use C++11 standard
  * Part 2: Missing menus on MacOS was due to a PyQt/MacOS bug regarding dynamic menus
* HDF5 file format: when importing an HDF5 dataset as a signal or an image, the
  dataset attributes were systematically copied to signal/image metadata: we now
  only copy the attributes which match standard data types (integers, floats, strings)
  to avoid errors when serializing/deserializing the signal/image object
* Installation/configuration viewer: improved readability (removed syntax highlighting)
* PyInstaller specification file: added missing `skimage` data files manually in order
  to continue supporting Python 3.8 (see [Issue #12](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/12) - Stand-alone version on Windows 7: missing `api-ms-win-core-path-l1-1-0.dll`)
* Fixed [Issue #13](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/13) - ArchLinux: `qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found`

## DataLab Version 0.9.2 ##

🛠️ Bug fixes:

* Region of interest (ROI) extraction feature for images:
  * ROI extraction was not working properly when the "Extract all regions of interest
    into a single image object" option was enabled if there was only one defined ROI.
    The result was an image positioned at the origin (0, 0) instead of the expected
    position (x0, y0) and the ROI rectangle itself was not removed as expected.
    This is now fixed (see [Issue #6](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/6) - 'Extract multiple ROI' feature: unexpected result for a single ROI)
  * ROI rectangles with negative coordinates were not properly handled:
    ROI extraction was raising a `ValueError` exception, and the image mask was not
    displayed properly.
    This is now fixed (see [Issue #7](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/7) - Image ROI extraction: `ValueError: zero-size array to reduction operation minimum which has no identity`)
  * ROI extraction was not taking into account the pixel size (dx, dy) and the origin
    (x0, y0) of the image.
    This is now fixed (see [Issue #8](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/8) - Image ROI extraction: take into account pixel size)
* Macro-command console is now read-only:
  * The macro-command panel Python console is currently not supporting standard input
    stream (`stdin`) and this is intended (at least for now)
  * Set Python console read-only to avoid confusion

## DataLab Version 0.9.1 ##

🛠️ Bug fixes:

* French translation is not available on Windows/Stand alone version:
  * Locale was not properly detected on Windows for stand-alone version (frozen
    with `pyinstaller`) due to an issue with `locale.getlocale()` (function
    returning `None` instead of the expected locale on frozen applications)
  * This is ultimately a `pyinstaller` issue, but a workaround has been
    implemented in `guidata` V3.2.2 (see [guidata issue #68](https://github.com/PlotPyStack/guidata/issues/68) - Windows: gettext translation is not working on frozen applications)
  * [Issue #2](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/2) - French translation is not available on Windows Stand alone version
* Saving image to JPEG2000 fails for non integer data:
  * JPEG2000 encoder does not support non integer data or signed integer data
  * Before, DataLab was showing an error message when trying to save incompatible
    data to JPEG2000: this was not a consistent behavior with other standard image
    formats (e.g. PNG, JPG, etc.) for which DataLab was automatically converting
    data to the appropriate format (8-bit unsigned integer)
  * Current behavior is now consistent with other standard image formats: when
    saving to JPEG2000, DataLab automatically converts data to 8-bit unsigned
    integer or 16-bit unsigned integer (depending on the original data type)
  * [Issue #3](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/3) - Save image to JPEG2000: 'OSError: encoder error -2 when writing image file'
* Windows stand-alone version shortcuts not showing in current user start menu:
  * When installing DataLab on Windows from a non-administrator account, the
    shortcuts were not showing in the current user start menu but in the
    administrator start menu instead (due to the elevated privileges of the
    installer and the fact that the installer does not support installing
    shortcuts for all users)
  * Now, the installer *does not* ask for elevated privileges anymore, and
    shortcuts are installed in the current user start menu (this also means that
    the current user must have write access to the installation directory)
  * In future releases, the installer will support installing shortcuts for all
    users if there is a demand for it (see [Issue #5](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/5))
  * [Issue #4](https://github.com/Codra-Ingenierie-Informatique/DataLab/issues/4) - Windows: stand-alone version shortcuts not showing in current user start menu
* Installation and configuration window for stand-alone version:
  * Do not show ambiguous error message 'Invalid dependencies' anymore
  * Dependencies are supposed to be checked when building the stand-alone version
* Added PDF documentation to stand-alone version:
  * The PDF documentation was missing in previous release
  * Now, the PDF documentation (in English and French) is included in the
    stand-alone version

## DataLab Version 0.9.0 ##

New dependencies:

* DataLab is now powered by [PlotPyStack](https://github.com/PlotPyStack):
  * [PythonQwt](https://github.com/PlotPyStack/PythonQwt)
  * [guidata](https://github.com/PlotPyStack/guidata)
  * [PlotPy](https://github.com/PlotPyStack/PlotPy)
* [opencv-python](https://pypi.org/project/opencv-python/) (algorithms for image processing)

New reference platform:

* DataLab is validated on Windows 11 with Python 3.11 and PyQt 5.15
* DataLab is also compatible with other OS (Linux, MacOS) and other Python-Qt
  bindings and versions (Python 3.8-3.12, PyQt6, PySide6)

New features:

* DataLab is a platform:
  * Added support for plugins
    * Custom processing features available in the "Plugins" menu
    * Custom I/O features: new file formats can be added to the standard I/O
      features for signals and images
    * Custom HDF5 features: new HDF5 file formats can be added to the standard
      HDF5 import feature
    * More features to come...
  * Added remote control feature: DataLab can be controlled remotely via a
    TCP/IP connection (see [Remote control](https://cdlapp.readthedocs.io/en/latest/remote_control.html))
  * Added macro commands: DataLab can be controlled via a macro file (see
    [Macro commands](https://cdlapp.readthedocs.io/en/latest/macro_commands.html))
* General features:
  * Added settings dialog box (see "Settings" entry in "File" menu):
    * General settings
    * Visualization settings
    * Processing settings
    * Etc.
  * New default layout: signal/image panels are on the right side of the main
    window, visualization panels are on the left side with a vertical toolbar
* Signal/Image features:
  * Added process isolation: each signal/image is processed in a separate
    process, so that DataLab does not freeze anymore when processing large
    signals/images
  * Added support for groups: signals and images can be grouped together, and
    operations can be applied to all objects in a group, or between groups
  * Added warning and error dialogs with detailed traceback links to the source
    code (warnings may be optionally ignored)
  * Drastically improved performance when selecting objects
  * Optimized performance when showing large images
  * Added support for dropping files on signal/image panel
  * Added "Computing parameters" group box to show last result input parameters
  * Added "Copy titles to clipboard" feature in "Edit" menu
  * For every single processing feature (operation, processing and computing menus),
    the entered parameters (dialog boxes) are stored in cache to be used as defaults
    the next time the feature is used
* Signal processing:
  * Added support for optional FFT shift (see Settings dialog box)
* Image processing:
  * Added pixel binning operation (X/Y binning factors, operation: sum, mean, ...)
  * Added "Distribute on a grid" and "Reset image positions" in operation menu
  * Added Butterworth filter
  * Added exposure processing features:
    * Gamma correction
    * Logarithmic correction
    * Sigmoïd correction
  * Added restoration processing features:
    * Total variation denoising filter (TV Chambolle)
    * Bilateral filter (denoising)
    * Wavelet denoising filter
    * White Top-Hat denoising filter
  * Added morphological transforms (disk footprint):
    * White Top-Hat
    * Black Top-Hat
    * Erosion
    * Dilation
    * Opening
    * Closing
  * Added edge detection features:
    * Roberts filter
    * Prewitt filter (vertical, horizontal, both)
    * Sobel filter (vertical, horizontal, both)
    * Scharr filter (vertical, horizontal, both)
    * Farid filter (vertical, horizontal, both)
    * Laplace filter
    * Canny filter
  * Contour detection: added support for polygonal contours (in addition to
    circle and ellipse contours)
  * Added circle Hough transform (circle detection)
  * Added image intensity levels rescaling
  * Added histogram equalization
  * Added adaptative histogram equalization
  * Added blob detection methods:
    * Difference of Gaussian
    * Determinant of Hessian method
    * Laplacian of Gaussian
    * Blob detection using OpenCV
  * Result shapes and annotations are now transformed (instead of removed) when
    executing one of the following operations:
    * Rotation (arbitrary angle, +90°, -90°)
    * Symetry (vertical/horizontal)
  * Added support for optional FFT shift (see Settings dialog box)
* Console: added configurable external editor (default: VSCode) to follow the
  traceback links to the source code
