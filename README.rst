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

``cmpdata`` is installable using ``conda`` or ``pip``. Conda installation is simple as:

.. code-block::
	conda install -c thassan cmpdata

For ``pip`` installation, you have to first install dependencies
 ::
    conda install -c conda-forge dask netCDF4
    conda install -c conda-forge xesmf esmpy=7.1.0
    pip install cmpdata

Alternatively, use the yml files in ci directory to create appropriate environement
 ::
    conda env create --file environment-py37.yml
    source activate cmdata
    pip install cmpdata

Requires python v3.6 or v3.7 and supports both Mac and Linux. Windows users can use `Windows Subsystem`_.

.. _`Windows Subsystem`: https://docs.microsoft.com/en-us/windows/wsl/install-win10


License
-------

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://opensource.org/licenses/MIT
