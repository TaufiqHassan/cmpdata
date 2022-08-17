Quickstart guide
================

A basic user guide for minimal usage.

Use conda to install from your terminal - 

``conda install -c thassan cmpdata`` 

General usage -

- Type ``cmpdata -h`` for help message.
- Use ``cmpdata -o info`` to get information on the raw data.
- Use ``cmpdata -o rm`` to produce realization means.
- Use ``cmpdata -o mm`` to produce model means.
- Use ``cmpdata -o stats`` to apply statistics.

All usable arguments and their explanations (as of v2.0.1) - ::

    options:
    -h, --help            show this help message and exit
    -o {info,rm,mm,stats,ts}, --output-options {info,rm,mm,stats,ts}
            Select an output option
    -dir DIR              Select directory.
    -m M                  Model names (multiple comma separated model names are allowed)
    -e E                  Experiment names (multiple comma separated experiments are allowed)
    -v V                  Variable names (multiple comma separated variables are allowed)
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

**Example usage 1** ::

    $ cmpdata -o info -dir /data/directory/here

**Example output 1** ::

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

**Example usage 2** ::

    $ cmpdata -o rm -dir /data/directory/here -v rlut,rsut -e ssp370 -m UKESM1-0-LL -t -regrid on

**Example output 2** ::

    For variable / model / experiment:  rlut / UKESM1-0-LL / ssp370

    Available realizations: ['r1i1p1f2' 'r2i1p1f2' 'r3i1p1f2']
    
    calculating for:  r1i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r1i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r1i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (1032, 144, 192)
    
    calculating for:  r2i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r2i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r2i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (1032, 144, 192)
    
    calculating for:  r3i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r3i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r3i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (1032, 144, 192)
    
    Getting tmean
    new shape: (86, 144, 192)
    Reuse existing file: bilinear_144x192_180x360_peri.nc
    
    Ensemble data shape: (86, 180, 360)
    [########################################] | 100% Completed |  1.5s
    
    For variable / model / experiment:  rsut / UKESM1-0-LL / ssp370
    
    Available realizations: ['r1i1p1f2' 'r2i1p1f2' 'r3i1p1f2']
    
    calculating for:  r1i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rsut_Amon_UKESM1-0-LL_ssp370_r1i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rsut_Amon_UKESM1-0-LL_ssp370_r1i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (1032, 144, 192)
    
    calculating for:  r2i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rsut_Amon_UKESM1-0-LL_ssp370_r2i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rsut_Amon_UKESM1-0-LL_ssp370_r2i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (1032, 144, 192)
    
    calculating for:  r3i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rsut_Amon_UKESM1-0-LL_ssp370_r3i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rsut_Amon_UKESM1-0-LL_ssp370_r3i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (1032, 144, 192)
    
    Getting tmean
    new shape: (86, 144, 192)
    Reuse existing file: bilinear_144x192_180x360_peri.nc
    
    Ensemble data shape: (86, 180, 360)
    [########################################] | 100% Completed |  1.7s
    Finished in 5.28 second(s)


**Example usage 3** ::

    $ cmpdata -o mm -dir /data/directory/here -v rlut -e ssp370 -m MRI-ESM2-0,UKESM1-0-LL,GISS-E2-1-G -rm -out rlut_model_mean_output_file_2015-2020.nc -init 2015 -end 2020

**Example output 3** ::

    For variable / model / experiment:  rlut / GISS-E2-1-G / ssp370
    
    Available realizations: ['r1i1p1f2' 'r1i1p3f1' 'r1i1p3f2' 'r1i1p5f1' 'r2i1p1f2' 'r2i1p3f1'
     'r2i1p3f2' 'r2i1p5f1' 'r3i1p1f2' 'r3i1p3f1' 'r3i1p3f2' 'r3i1p5f1']
    
    calculating for:  r1i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p1f2_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p1f2_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r1i1p3f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p3f1_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p3f1_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r1i1p3f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p3f2_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p3f2_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r1i1p5f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p5f1_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r1i1p5f1_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r2i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p1f2_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p1f2_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r2i1p3f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p3f1_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p3f1_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r2i1p3f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p3f2_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p3f2_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r2i1p5f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p5f1_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r2i1p5f1_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r3i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p1f2_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p1f2_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r3i1p3f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p3f1_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p3f1_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r3i1p3f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p3f2_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p3f2_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    calculating for:  r3i1p5f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p5f1_gn_201501-205012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_GISS-E2-1-G_ssp370_r3i1p5f1_gn_205101-210012.nc')]
    
    Data shape: (72, 90, 144)
    
    Ensemble data shape: (72, 90, 144)
    [########################################] | 100% Completed |  0.5s
    Create weight file: bilinear_90x144_180x360_peri.nc
    
    For variable / model / experiment:  rlut / MRI-ESM2-0 / ssp370
    
    Available realizations: ['r1i1p1f1' 'r3i1p1f1' 'r5i1p1f1']
    
    calculating for:  r1i1p1f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_MRI-ESM2-0_ssp370_r1i1p1f1_gn_201501-210012.nc')]
    
    Data shape: (72, 160, 320)
    
    calculating for:  r3i1p1f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_MRI-ESM2-0_ssp370_r3i1p1f1_gn_201501-210012.nc')]
    
    Data shape: (72, 160, 320)
    
    calculating for:  r5i1p1f1
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_MRI-ESM2-0_ssp370_r5i1p1f1_gn_201501-210012.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_MRI-ESM2-0_ssp370_r5i1p1f1_gn_201501-210012_annual.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_MRI-ESM2-0_ssp370_r5i1p1f1_gn_201501-210012_modAnom.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_MRI-ESM2-0_ssp370_r5i1p1f1_gn_201501-210012_monClim.nc')]
    
    Found issue on r5i1p1f1 realization of MRI-ESM2-0
    
    Ignoring r5i1p1f1
    
    Ensemble data shape: (72, 160, 320)
    [########################################] | 100% Completed |  0.2s
    Reuse existing file: bilinear_160x320_180x360_peri.nc
    
    For variable / model / experiment:  rlut / UKESM1-0-LL / ssp370
    
    Available realizations: ['r1i1p1f2' 'r2i1p1f2' 'r3i1p1f2']
    
    calculating for:  r1i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r1i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r1i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (72, 144, 192)
    
    calculating for:  r2i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r2i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r2i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (72, 144, 192)
    
    calculating for:  r3i1p1f2
    [PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r3i1p1f2_gn_201501-204912.nc')
     PosixPath('/Volumes/HD4/mechanism/SDF/rlut_Amon_UKESM1-0-LL_ssp370_r3i1p1f2_gn_205001-210012.nc')]
    
    Data shape: (72, 144, 192)
    
    Ensemble data shape: (72, 144, 192)
    [########################################] | 100% Completed |  0.2s
    Reuse existing file: bilinear_144x192_180x360_peri.nc
    
    Ensemble data shape: (72, 180, 360)
    Finished in 9.55 second(s)

**Example usage 4** ::

    $ cmpdata -o stats -trend -f rlut_model_mean_output_file_2015-2020.nc -v rlut -dir /data/directory/here -init 2015 -end 2020

Example output 4 is a spatial trend and significance (2015-2020) 2D file named ``rlut_model_mean_output_file_2015_trend.nc``.

``ncdump -h rlut_model_mean_output_file_2015-2020_trend.nc`` ::

    netcdf rlut_model_mean_output_file_2015-2020_trend {
    dimensions:
    	lat = 180 ;
    	lon = 360 ;
    variables:
    	double lat(lat) ;
    		lat:_FillValue = NaN ;
    	double lon(lon) ;
    		lon:_FillValue = NaN ;
    	double trend(lat, lon) ;
    		trend:_FillValue = NaN ;
    	byte sig(lat, lon) ;
    		sig:dtype = "bool" ;

