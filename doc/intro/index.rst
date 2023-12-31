Getting started
===============

DataLab in a nutshell
---------------------

DataLab is an open platform for signal and image processing.
Its functional scope is intentionally broad. With its many functions,
some of them technically advanced, DataLab enables the processing and
visualization of all types of scientific data. As a result, scientific,
industrial, and innovation stakeholders can have access to an
easy-to-use tool that is simple to adapt and offers the reliability
of industrial-grade software.

What are the applications for Datalab?
--------------------------------------

Real world examples
^^^^^^^^^^^^^^^^^^^

A few concrete and specific examples illustrate the nature of the work
that can be carried out with DataLab:

- Processing of experimental signals acquired on a scientific facility
- Automatic detection laser spot positions in a scene
- Instrument alignment through image processing
- Automatic pattern detection and geometric corrections

.. _usage_modes:

Usage modes
^^^^^^^^^^^

Depending on the application, DataLab can be used in three different modes:

- **Stand-alone mode**: DataLab is a full-fledged processing application that
  can be adapted to the client's needs through the addition of
  industry-specific plugins.
- **Embedded mode**: DataLab is integrated into your application to provide
  the necessary processing and visualization features.
- **Remote-controlled mode**: DataLab communicates with your application,
  allowing it to benefit from its functionality without disrupting
  the user experience.

.. note::

    DataLab can also be controlled from your familiar development environment
    (e.g., Visual Studio Code, Spyder, ...) to perform calculations using
    your processing functions while leveraging the advanced features of DataLab.

With its user-friendly experience and versatile usage modes, DataLab enables
efficient development of your data processing and visualization applications
while benefiting from an industrial-grade technological platform.

How does DataLab work?
----------------------

DataLab is a platform for data processing and visualization (signals or images)
that includes many functions. Developed in Python, it benefits from the
richness of the associated ecosystem in terms of scientific and
technical libraries.

.. _main_features:

Main features
^^^^^^^^^^^^^

The main technical features of DataLab include:

- Support for numerous standard and proprietary data formats
- Opening an arbitrary number of objects (signals or images) for batch
  processing, with the possibility of defining groups of objects
- Simultaneous viewing of multiple objects with annotation support
- Standard operations and processing on signals and images
- Advanced image processing (restoration, morphology, edge detection, etc.)
- Management of multiple regions of interest (calculations, extractions)
- Macro-command editor
- Remote-controllable API
- Embedded interactive Python console

.. _key_strengths:

Key strengths
^^^^^^^^^^^^^

DataLab highlights four key strengths:

1. **Extensibility**: The DataLab plugin system makes it easy to code new
   features (specific processing, specific file formats, custom graphical
   interfaces). It can also be used as a customizable platform.

2. **Interoperability**: DataLab can also be embedded in your own application.
   For example, within data processing software, machine-level control systems,
   or test bench applications.

3. **Automation**: a high-level public API allows for full remote control of
   DataLab to open and process data.

4. **Maintainability and testability**: DataLab is an industrial-grade
   scientific and technical processing software. The built-in automated tests
   in DataLab cover 90% of its features, which is significant for software
   with graphical interfaces and helps mitigate regression risks.

Researchers, engineers, scientists, you will undoubtedly benefit from the
capabilities of DataLab. Its open-source software model will also allow you
to reinvest your achievements in the open-source community, of which any
reputable publisher should be an active member.


.. toctree::
   :maxdepth: 2
   :hidden:

   installation
   overview
