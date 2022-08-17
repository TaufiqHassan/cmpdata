.. cmpdata documentation master file, created by
   sphinx-quickstart on Sat Aug 17 15:52:39 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

cmpdata documentation
======================

``cmpdata`` is a python-based pre-processor for the 6th Coupled Model Intercomparison Project (`CMIP6`_) raw data. It is often cumbersome to handle MIP data considering the number of variables, models and experments often used for a project! Multiple realizations/ensembles can make the total data size pretty large and even harder to handle. Users often save data in multiple directories, which makes handling them more time consuming. With ``cmpdata``, users can forget about rearranging data into multiple directories and processing data from them separately. It can produce comprehensive information with list of variables, models and experiments of raw NetCDF data available in a directory and then pre-process them as necessary.'

Features
--------

- Handle raw CMIP6 data
- Analyze any specific models/experiments/variables
- Perform regridding for model ensemble means
- Data preprocessing
- Statistical analysis 

Useful links
------------

- Source code is available on `GitHub`_.
- A `quickstart guide`_ is available.
- `Overview`_ of the CMIP6 experimental design and organization.


User guide
----------

.. toctree::
   :maxdepth: 2

   guide/quickstart
   guide/install
   guide/get_info
   guide/authors.rst
   guide/license


.. _`CMIP6`: https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6
.. _`GitHub`: https://github.com/TaufiqHassan/cmpdata
.. _`quickstart guide`: https://github.com/TaufiqHassan/cmpdata/blob/master/README.rst
.. _`Overview`: https://www.geosci-model-dev.net/9/1937/2016/gmd-9-1937-2016.html

