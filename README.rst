===============================
Handle CMIP6
===============================

.. image:: https://img.shields.io/travis/TaufiqHassan/cmpdata.svg
        :target: https://travis-ci.org/TaufiqHassan/cmpdata

.. image:: https://img.shields.io/pypi/v/cmpdata.svg
        :target: https://pypi.python.org/pypi/cmpdata


``cmpdata`` package can handle and analyze raw CMIP6 data.

* GitHub repo: https://github.com/TaufiqHassan/cmpdata
* Documentation: coming soon . . .

Features
--------

- Handle raw CMIP6 data
- Analyze any specific models/experiments/variables
- Perform regridding for model ensemble means
- Data preprocessing 
- Statistical analysis (coming soon)

Installation
------------

``cmpdata`` is installable using ``conda`` or ``pip``. Conda installation is simple as: ::

	conda install -c thassan cmpdata

For ``pip`` installation, you have to first install dependencies: ::

    conda install -c conda-forge dask netCDF4
    conda install -c conda-forge xesmf esmpy=7.1.0
    pip install cmpdata

Alternatively, use the yml files in ci directory to create appropriate environement: ::

    conda env create --file environment-py37.yml
    source activate cmdata
    pip install cmpdata

Requires python v3.6 or v3.7 and supports both Mac and Linux. Windows users can use `Windows Subsystem`_.

.. _`Windows Subsystem`: https://docs.microsoft.com/en-us/windows/wsl/install-win10


Usage
------

``cmpdata`` can be used to handle and analyze raw CMIP6 data. A lot of the options available in ``acccmip6`` is available in ``cmpdata``, especially for selecting models, experiments and variables. 
``cmpdata`` also tries to be a good command-line interface (CLI). Run ``cmpdata -h`` to see a help message with all the arguments you can pass.

Required Arguments
------------------

- ``-o`` : Takes output type. 
         'info' for the files information (number of files, avaialble models, variables, experiments and realizations) in a directory,
         'rm' for performing ensemble realization means,
         'mm' for performing ensemble model mean and
         'stats' for performing statistical analysis.

Optional Arguments
------------------

- ``-dir`` : Selected directory
- ``-m`` : Model names (multiple comma separated names are allowed)
- ``-e`` : Experiment names
- ``-v`` : Variable names
- ``-r`` : Realizations
- ``-init`` : Initial year selection
- ``-end`` : Ending year selection
- ``-e2`` : Secondary experiment name
- ``-dir2`` : Selected directory for the second experiment
- ``-t`` : Temporal mean option
- ``-s`` : Seasonal mean option (use in conjunction with ``-t`` option)
- ``-f`` : Temporal mean fequency (use in conjunction with ``-t`` option)
- ``-rm`` : Use the realization means
- ``-curve`` : Regridding to curvilinear grids

License
-------

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://opensource.org/licenses/MIT
