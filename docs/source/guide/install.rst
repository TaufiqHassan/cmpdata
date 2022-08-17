Installation
============

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

Using alternative method will cause usrs to invoke ``cmpdata`` as ``python <cmpdata directory>/cmpdata.py``.

Supports both OSX and Linux. Windows users can use `Windows Subsystem`_. Check installation with -

``cmpdata -h``; which should produce the help message with all available options (shown for features available in v2.0.1) ::

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
        -reg REG              Select region for timeseries output (choices: NH/SH/NH-mid/SH-mid/NH-pole/SH-pole/NA/NAT/CONUS)
        -rm                   Use the realization means
        -a                    Use cell areas for spatial mean calculations
        -curve                Regridding to curvilinear grids
        -w                    All model means as ens dim (used by -std, -mm, -aggr stats options)
        -ci CI                confidence interval used in -trend and -aggr options
        -regrid               regridding on/off
        

.. _`Windows Subsystem`: https://docs.microsoft.com/en-us/windows/wsl/install-win10
