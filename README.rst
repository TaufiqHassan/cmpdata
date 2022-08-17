===============================
Pre-process CMIP6 data
===============================

.. image:: https://img.shields.io/travis/TaufiqHassan/cmpdata.svg
        :target: https://travis-ci.org/TaufiqHassan/cmpdata

.. image:: https://img.shields.io/pypi/v/cmpdata.svg
        :target: https://pypi.python.org/pypi/cmpdata

.. image:: https://zenodo.org/badge/295042856.svg
   :target: https://zenodo.org/badge/latestdoi/295042856
   
``cmpdata`` package can handle and analyze raw CMIP6 data.

* GitHub repo: https://github.com/TaufiqHassan/cmpdata

Features
--------

- Handle raw CMIP6 data
- Analyze any specific models/experiments/variables
- Perform regridding for model ensemble means
- Data preprocessing 
- Statistical analysis 

Installation
------------

Installation via conda -

``conda install -c thassan cmpdata``

Requires python v3.6 or v3.7. Make sure you have added the conda-forge channel in your environment.  ::

        conda create --name cmpdata python=3.7 (or 3.6)
        conda activate cmpdata
        conda config --env --add channels conda-forge
        conda install -c thassan cmpdata 

Alternatively, use the YAML file to create a virtual conda enviroment (cmpdata)

``conda env create -f environment.yml``

And then activate cmpdata to use cmpdata

``conda activate cmpdata``

Supports both OSX and Linux. Windows users can use `Windows Subsystem`_.

.. _`Windows Subsystem`: https://docs.microsoft.com/en-us/windows/wsl/install-win10


Usage
------

``cmpdata`` can be used to handle and analyze raw CMIP6 data. A lot of the options available in ``acccmip6`` is available in ``cmpdata``, especially for selecting models, experiments and variables. 
``cmpdata`` also tries to be a good command-line interface (CLI). Run ``cmpdata -h`` to see a help message with all the arguments you can pass.

``cmpdata -h`` ::

        usage: cmpdata.py [-h] -o {info,rm,mm,stats,ts} [-dir DIR] [-m M] [-e E] [-v V] [-r R] [-out OUT] [-f F] [-init INIT] [-end END] [-t] [-z] [-s S] [-mm]
        [-std] [-clim] [-anom] [-manom] [-trend] [-aggr] [-freq FREQ] [-reg REG] [-rm] [-a] [-curve] [-w] [-ci CI] [-regrid]

        options:
        -h, --help            show this help message and exit
        -o {info,rm,mm,stats,ts}, --output-options {info,rm,mm,stats,ts}
                Select an output option
        -dir DIR              Select directory.
        -m M                  Model names
        -e E                  Experiment names
        -v V                  Variable names
        -r R                  Realization
        -out OUT              Output file name
        -f F                  Input filenames for stats
        -init INIT            Initial year
        -end END              Ending year
        -t                    Temporal mean option
        -z                    Zonal mean option
        -s S                  Seasonal mean option
        -mm                   Calculate model ensemble mean
        -std                  Calculate model std
        -clim                 Calculate monthly climatology
        -anom                 Calculate monthly anomaly
        -manom                Calculate model anomaly
        -trend                Calculate variable grid-by-grid trends
        -aggr                 Calculate model aggreement
        -freq FREQ            Temporal mean frequency: annual/daily/monthly
        -reg REG              Select region for timeseries output
        -rm                   Use the realization means
        -a                    Use cell areas for spatial mean calculations
        -curve                Regridding to curvilinear grids
        -w                    All model means as ens dim (used by -std, -mm, -aggr stats options)
        -ci CI                confidence interval used in -trend and -aggr options
        -regrid               regridding on/off


License
-------

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://opensource.org/licenses/MIT
