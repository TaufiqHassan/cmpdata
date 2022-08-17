Extract data info.
==================

To extract information of the available CMIP6 data archived in a directory. This information includes the number of variables, models, experiments, realizations, and data files available in a directory.

It is a helpful feature, where users can put all their raw data in a single directory. This relieves the requirement to make directories for different variables/experiments or so on and remember them while performing pre-processing.

**General usage:**  ::

        $ cmpdata -o info -dir /directory/path/here

**output** ::

    <<Showing all available data>>
    
    
    Available 34 variables: ['areacella' 'areacello' 'clt' 'evs' 'evspsbl' 'fsitherm' 'hfbasin' 'hfds'
     'mlotst' 'msftmz' 'msftyz' 'pr' 'psl' 'rlds' 'rlus' 'rlut' 'rlutcs'
     'rsds' 'rsdt' 'rsus' 'rsut' 'rsutcs' 'sfcWind' 'sftlf' 'siconc' 'siconca'
     'sltovgyre' 'sltovovrt' 'sos' 'sowaflup' 'sowflisf' 'tos' 'tosC' 'wfo']
    
    Available 4 models: ['EC-Earth3-AerChem' 'GISS-E2-1-G' 'MRI-ESM2-0' 'UKESM1-0-LL']
    
    Available 7 experiments: ['piControl' 'ssp370-lowNTCF' 'ssp370-lowNTCFCH4' 'ssp370'
     'ssp370SST-lowNTCF' 'ssp370SST-lowNTCFCH4' 'ssp370SST']
    
    Available 20 realizations: ['r1i1p1f1' 'r1i1p3f1' 'r1i1p1f2' 'r1i1p5f1' 'r2i1p3f1' 'r3i1p3f1'
     'r3i1p1f1' 'r5i1p1f1' 'r2i1p1f2' 'r3i1p1f2' 'r1i1p3f2' 'r1i2p1f1'
     'r2i1p3f2' 'r3i1p3f2' 'r1i1p2f2' 'r2i1p2f2' 'r3i1p2f2' 'r2i1p5f1'
     'r3i1p5f1' 'r2i1p1f1']
    
    Total number of files: 7801
    
This single directory contains ~7800 CMIP6 raw fies! These are from different models and experiments. Users can pin-point on the number of data for a particular model/experiment/variable using ``-m`` or ``-e`` or ``-v`` options.

**Example usage:** ::

    $ cmpdata -o info -dir /directory/path/here -m UKESM1-0-LL -e ssp370 -v rlut

**output** ::

    Available 1 variables: ['rlut']
    
    Available 1 models: ['UKESM1-0-LL']
    
    Available 1 experiments: ['ssp370']
    
    Available 3 realizations: ['r1i1p1f2' 'r2i1p1f2' 'r3i1p1f2']
    
    Total number of files: 6 
    
So, there are 3 realizations of ``rlut`` for ``'UKESM1-0-LL`` model in ``ssp370`` experiment. Total number of files is 6, meaning each realization has 2 files. So, user can decide whether he has all the files before applying pre-processing.
    
