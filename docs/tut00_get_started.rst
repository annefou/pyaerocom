
Getting started
~~~~~~~~~~~~~~~

This notebook is meant to give a quick introduction into pyaerocom based
and into some of the relevant features and workflows when using
`pyaerocom <http://aerocom.met.no/pyaerocom/>`__.

It ends with a colocation of CAM53-Oslo model AODs both all-sky and
clear-sky with Aeronet Sun V3 level 2 data.

Pyaerocom API flowchart (minimal)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following flowchart illustrates the minimal workflow to create
standard output in pyaerocom based on a user query (that typically
comprises a model ID and observation ID as well as one (or more)
variable(s) of interest (products indicated in red are not available
yet, date of latest update: 4-10-2018).

.. code:: ipython3

    from IPython.display import Image
    flowchart = Image(filename=('../suppl/api_minimal_v0.png'))
    flowchart




.. image:: tut00_get_started/tut00_get_started_2_0.png



A user query typically comprises a model (+ experiment -> model run) and
an observation network, which are supposed to be compared.

**Note**: the flowchart depicts a situation, where the data from the
observation network is *ungridded*, that is, the data is not available
in a gridded format such as NetCDF, but, for instance, in the form of
column seperated text files (as is the case for Aeronet data, which is
used as an example here and included in the test dataset). For
``gridded`` observations (e.g. satellite data), the flowchart is
equivalent but with ``ReadGridded`` class and ``GriddedData`` for the
observation branch (and without caching).

This notebook illustrates and briefly discusses the individual aspects
displayed in the flowchart.

.. code:: ipython3

    import pyaerocom as pya

Check data directory
''''''''''''''''''''

By default, pyaerocom assumes that the AEROCOM database can be accessed
(cf. top of flowchart), that is, it initiates all data query paths
relative to the database server path names.

.. code:: ipython3

    pya.const.BASEDIR




.. parsed-literal::

    '/lustre/storeA/project/aerocom/'



**NOTE**: Execution of the following lines will only work if you are
connected to the AEROCOM data server or if you have access to the
pyaerocom testdataset. The latter can be retrieved upon request (please
contact jonasg@met.no).

Reading of and working with *gridded* model data (``ReadGridded`` and ``GriddedData`` classes)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section illustrates the reading of gridded data as well as some
features of the ``GriddedData`` class of *pyaerocom*. First, however, we
have to find a valid model ID for the reading (cf. flow chart).

Find model data
'''''''''''''''

The database contains data from the CAM53-Oslo model, which is used in
the following. You can use the ``browse_database`` function of pyaerocom
to find model ID’s (which can be quite cryptic sometimes) using wildcard
pattern search.

.. code:: ipython3

    pya.browse_database('CAM53*-Oslo*UNTUNED*')


.. parsed-literal::

    
    Pyaerocom ReadGridded
    ---------------------
    Model ID: CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PI_UNTUNED
    Data directory: /lustre/storeA/project/aerocom/aerocom2/NorESM_SVN_TEST/CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PI_UNTUNED/renamed
    Available variables: ['abs440aer', 'abs440aercs', 'abs500aer', 'abs5503Daer', 'abs550aer', 'abs550bc', 'abs550dryaer', 'abs550dust', 'abs550oa', 'abs550so4', 'abs550ss', 'abs670aer', 'abs870aer', 'airmass', 'area', 'asy3Daer', 'bc5503Daer', 'cheaqpso4', 'chegpso4', 'chepso2', 'cl3D', 'clt', 'drybc', 'drydms', 'drydust', 'dryoa', 'dryso2', 'dryso4', 'dryss', 'ec5503Daer', 'ec550dryaer', 'emibc', 'emidms', 'emidust', 'emioa', 'emiso2', 'emiso4', 'emiss', 'hus', 'landf', 'loadbc', 'loaddms', 'loaddust', 'loadoa', 'loadso2', 'loadso4', 'loadss', 'mmraerh2o', 'mmrbc', 'mmrdu', 'mmroa', 'mmrso4', 'mmrss', 'od440aer', 'od440csaer', 'od550aer', 'od550aerh2o', 'od550bc', 'od550csaer', 'od550dust', 'od550lt1aer', 'od550lt1dust', 'od550oa', 'od550so4', 'od550ss', 'od670aer', 'od870aer', 'od870csaer', 'orog', 'precip', 'pressure', 'ps', 'rlds', 'rlus', 'rlut', 'rlutcs', 'rsds', 'rsdscs', 'rsdt', 'rsus', 'rsut', 'sconcbc', 'sconcdms', 'sconcdust', 'sconcoa', 'sconcso2', 'sconcso4', 'sconcss', 'temp', 'vmrdms', 'vmrso2', 'wetbc', 'wetdms', 'wetdust', 'wetoa', 'wetso2', 'wetso4', 'wetss']
    Available years: [9999]
    Available time resolutions ['monthly']
    
    Pyaerocom ReadGridded
    ---------------------
    Model ID: CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED
    Data directory: /lustre/storeA/project/aerocom/aerocom2/NorESM_SVN_TEST/CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED/renamed
    Available variables: ['abs440aer', 'abs440aercs', 'abs500aer', 'abs5503Daer', 'abs550aer', 'abs550aercs', 'abs550bc', 'abs550dryaer', 'abs550dust', 'abs550oa', 'abs550so4', 'abs550ss', 'abs670aer', 'abs870aer', 'airmass', 'ang4487aer', 'ang4487csaer', 'area', 'asy3Daer', 'bc5503Daer', 'cheaqpso4', 'chegpso4', 'chepso2', 'cl3D', 'clt', 'drybc', 'drydms', 'drydust', 'dryoa', 'dryso2', 'dryso4', 'dryss', 'ec5503Daer', 'ec550dryaer', 'emibc', 'emidms', 'emidust', 'emioa', 'emiso2', 'emiso4', 'emiss', 'hus', 'landf', 'loadbc', 'loaddms', 'loaddust', 'loadoa', 'loadso2', 'loadso4', 'loadss', 'mmraerh2o', 'mmrbc', 'mmrdu', 'mmroa', 'mmrso4', 'mmrss', 'od440aer', 'od440csaer', 'od550aer', 'od550aerh2o', 'od550bc', 'od550csaer', 'od550dust', 'od550lt1aer', 'od550lt1dust', 'od550oa', 'od550so4', 'od550ss', 'od670aer', 'od870aer', 'od870csaer', 'orog', 'precip', 'pressure', 'ps', 'rlds', 'rlus', 'rlut', 'rlutcs', 'rsds', 'rsdscs', 'rsdt', 'rsus', 'rsut', 'sconcbc', 'sconcdms', 'sconcdust', 'sconcoa', 'sconcso2', 'sconcso4', 'sconcss', 'temp', 'vmrdms', 'vmrso2', 'wetbc', 'wetdms', 'wetdust', 'wetoa', 'wetso2', 'wetso4', 'wetss']
    Available years: [2004, 2005, 2006, 2007, 2008, 2009, 2010, 9999]
    Available time resolutions ['monthly']


Read Aerosol optical depth at 550 nm
''''''''''''''''''''''''''''''''''''

Import both clear-sky (*cs* in variable name) and all-sky data.

.. code:: ipython3

    reader = pya.io.ReadGridded('CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED')
    od550aer = reader.read_var('od550aer')
    od550csaer = reader.read_var('od550csaer')

Both data objects are instances of class
`GriddedData <http://aerocom.met.no/pyaerocom/api.html#module-pyaerocom.griddeddata>`__
which is based on the
`Cube <https://scitools.org.uk/iris/docs/v1.9.0/html/iris/iris/cube.html#iris.cube.Cube>`__
class (`iris
library <https://scitools.org.uk/iris/docs/v1.9.0/html/index.html>`__)
and features very similar functionality and more.

Some of these features are introduced below.

Overview of what is in the data
'''''''''''''''''''''''''''''''

Simply print the object.

.. code:: ipython3

    print(od550aer)


.. parsed-literal::

    pyaerocom.GriddedData: CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED
    Grid data: Aerosol optical depth at 500nm / (1) (time: 84; latitude: 192; longitude: 288)
         Dimension coordinates:
              time                            x             -               -
              latitude                        -             x               -
              longitude                       -             -               x
         Attributes:
              Conventions: CF-1.0
              NCO: 4.3.7
              Version: $Name$
              case: 53OSLO_PD_UNTUNED
              history: Thu Feb  9 11:05:21 2017: ncatted -O -a units,od550aer,o,c,1 /projects/NS2345K/CAM-Oslo/DO_AEROCOM/CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED/renamed/aerocom3_CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED_od550aer_Column_2004_monthly.nc
    Thu...
              host: hexagon-2
              initial_file: /work/shared/noresm/inputdata/atm/cam/inic/fv/cami-mam3_0000-01-01_0.9...
              logname: ihkarset
              nco_openmp_thread_number: 1
              revision_Id: $Id$
              source: CAM
              title: UNSET
              topography_file: /work/shared/noresm/inputdata/noresm-only/inputForNudging/ERA_f09f09_3...
         Cell methods:
              mean: time


.. code:: ipython3

    print(od550csaer)


.. parsed-literal::

    pyaerocom.GriddedData: CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED
    Grid data: Clear air Aerosol optical depth at 550nm / (1) (time: 84; latitude: 192; longitude: 288)
         Dimension coordinates:
              time                                      x             -               -
              latitude                                  -             x               -
              longitude                                 -             -               x
         Attributes:
              Conventions: CF-1.0
              NCO: 4.3.7
              Version: $Name$
              case: 53OSLO_PD_UNTUNED
              history: Thu Feb  9 11:05:16 2017: ncatted -O -a units,od550csaer,o,c,1 /projects/NS2345K/CAM-Oslo/DO_AEROCOM/CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED/renamed/aerocom3_CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED_od550csaer_Column_2004_monthly.nc
    Thu...
              host: hexagon-2
              initial_file: /work/shared/noresm/inputdata/atm/cam/inic/fv/cami-mam3_0000-01-01_0.9...
              logname: ihkarset
              nco_openmp_thread_number: 1
              revision_Id: $Id$
              source: CAM
              title: UNSET
              topography_file: /work/shared/noresm/inputdata/noresm-only/inputForNudging/ERA_f09f09_3...
         Cell methods:
              mean: time


Access time stamps
''''''''''''''''''

Time stamps are represented as numerical values with respect to a
reference date and frequency, according to the CF conventions. They can
be accessed via the ``time`` attribute of the data class.

.. code:: ipython3

    od550aer.time




.. parsed-literal::

    DimCoord(array([   0.,   31.,   60.,   91.,  121.,  152.,  182.,  213.,  244.,
            274.,  305.,  335.,  366.,  397.,  425.,  456.,  486.,  517.,
            547.,  578.,  609.,  639.,  670.,  700.,  731.,  762.,  790.,
            821.,  851.,  882.,  912.,  943.,  974., 1004., 1035., 1065.,
           1096., 1127., 1155., 1186., 1216., 1247., 1277., 1308., 1339.,
           1369., 1400., 1430., 1461., 1492., 1521., 1552., 1582., 1613.,
           1643., 1674., 1705., 1735., 1766., 1796., 1827., 1858., 1886.,
           1917., 1947., 1978., 2008., 2039., 2070., 2100., 2131., 2161.,
           2192., 2223., 2251., 2282., 2312., 2343., 2373., 2404., 2435.,
           2465., 2496., 2526.]), standard_name='time', units=Unit('days since 2004-01-01 00:00:00', calendar='standard'))



You may also want the time-stamps in the form of actual datetime-like
objects. These can be computed using the ``time_stamps()`` method:

.. code:: ipython3

    od550aer.time_stamps()




.. parsed-literal::

    array(['2004-01-01T00:00:00.000000', '2004-02-01T00:00:00.000000',
           '2004-03-01T00:00:00.000000', '2004-04-01T00:00:00.000000',
           '2004-05-01T00:00:00.000000', '2004-06-01T00:00:00.000000',
           '2004-07-01T00:00:00.000000', '2004-08-01T00:00:00.000000',
           '2004-09-01T00:00:00.000000', '2004-10-01T00:00:00.000000',
           '2004-11-01T00:00:00.000000', '2004-12-01T00:00:00.000000',
           '2005-01-01T00:00:00.000000', '2005-02-01T00:00:00.000000',
           '2005-03-01T00:00:00.000000', '2005-04-01T00:00:00.000000',
           '2005-05-01T00:00:00.000000', '2005-06-01T00:00:00.000000',
           '2005-07-01T00:00:00.000000', '2005-08-01T00:00:00.000000',
           '2005-09-01T00:00:00.000000', '2005-10-01T00:00:00.000000',
           '2005-11-01T00:00:00.000000', '2005-12-01T00:00:00.000000',
           '2006-01-01T00:00:00.000000', '2006-02-01T00:00:00.000000',
           '2006-03-01T00:00:00.000000', '2006-04-01T00:00:00.000000',
           '2006-05-01T00:00:00.000000', '2006-06-01T00:00:00.000000',
           '2006-07-01T00:00:00.000000', '2006-08-01T00:00:00.000000',
           '2006-09-01T00:00:00.000000', '2006-10-01T00:00:00.000000',
           '2006-11-01T00:00:00.000000', '2006-12-01T00:00:00.000000',
           '2007-01-01T00:00:00.000000', '2007-02-01T00:00:00.000000',
           '2007-03-01T00:00:00.000000', '2007-04-01T00:00:00.000000',
           '2007-05-01T00:00:00.000000', '2007-06-01T00:00:00.000000',
           '2007-07-01T00:00:00.000000', '2007-08-01T00:00:00.000000',
           '2007-09-01T00:00:00.000000', '2007-10-01T00:00:00.000000',
           '2007-11-01T00:00:00.000000', '2007-12-01T00:00:00.000000',
           '2008-01-01T00:00:00.000000', '2008-02-01T00:00:00.000000',
           '2008-03-01T00:00:00.000000', '2008-04-01T00:00:00.000000',
           '2008-05-01T00:00:00.000000', '2008-06-01T00:00:00.000000',
           '2008-07-01T00:00:00.000000', '2008-08-01T00:00:00.000000',
           '2008-09-01T00:00:00.000000', '2008-10-01T00:00:00.000000',
           '2008-11-01T00:00:00.000000', '2008-12-01T00:00:00.000000',
           '2009-01-01T00:00:00.000000', '2009-02-01T00:00:00.000000',
           '2009-03-01T00:00:00.000000', '2009-04-01T00:00:00.000000',
           '2009-05-01T00:00:00.000000', '2009-06-01T00:00:00.000000',
           '2009-07-01T00:00:00.000000', '2009-08-01T00:00:00.000000',
           '2009-09-01T00:00:00.000000', '2009-10-01T00:00:00.000000',
           '2009-11-01T00:00:00.000000', '2009-12-01T00:00:00.000000',
           '2010-01-01T00:00:00.000000', '2010-02-01T00:00:00.000000',
           '2010-03-01T00:00:00.000000', '2010-04-01T00:00:00.000000',
           '2010-05-01T00:00:00.000000', '2010-06-01T00:00:00.000000',
           '2010-07-01T00:00:00.000000', '2010-08-01T00:00:00.000000',
           '2010-09-01T00:00:00.000000', '2010-10-01T00:00:00.000000',
           '2010-11-01T00:00:00.000000', '2010-12-01T00:00:00.000000'],
          dtype='datetime64[us]')



Plotting maps
'''''''''''''

Maps of individual time stamps can be plotted using the quickplot_map
method.

.. code:: ipython3

    fig1 = od550aer.quickplot_map('2009-3-15')
    fig2 = od550csaer.quickplot_map('2009-3-15')



.. image:: tut00_get_started/tut00_get_started_23_0.png



.. image:: tut00_get_started/tut00_get_started_23_1.png


Filtering
'''''''''

Regional filtering can be performed using the
`Filter <http://aerocom.met.no/pyaerocom/api.html#module-pyaerocom.filter>`__
class (cf. flowchart above).

An overview of available default regions can be accessed via:

.. code:: ipython3

    print(pya.region.get_all_default_region_ids())


.. parsed-literal::

    ['WORLD', 'EUROPE', 'ASIA', 'AUSTRALIA', 'CHINA', 'INDIA', 'NAFRICA', 'SAFRICA', 'SAMERICA', 'NAMERICA']


Now let’s go for north Africa. Create instance of Filter class:

.. code:: ipython3

    f = pya.Filter('NAFRICA')
    f




.. parsed-literal::

    Filter([('_name', 'NAFRICA-wMOUNTAINS'),
            ('_region',
             Region NAFRICA Region([('_name', 'NAFRICA'), ('lon_range', [-20, 50]), ('lat_range', [0, 40]), ('lon_range_plot', [-20, 50]), ('lat_range_plot', [0, 40]), ('lon_ticks', None), ('lat_ticks', None)])),
            ('lon_range', [-20, 50]),
            ('lat_range', [0, 40]),
            ('alt_range', None)])



… and apply to the two data objects (this can be done by calling the
filter with the corresponding data class as input parameter):

.. code:: ipython3

    od550aer_nafrica = f(od550aer)
    od550csaer_nafrica = f(od550csaer)

Compare shapes:

.. code:: ipython3

    od550aer_nafrica




.. parsed-literal::

    pyaerocom.GriddedData
    Grid data: <iris 'Cube' of Aerosol optical depth at 500nm / (1) (time: 84; latitude: 42; longitude: 57)>



.. code:: ipython3

    od550aer




.. parsed-literal::

    pyaerocom.GriddedData
    Grid data: <iris 'Cube' of Aerosol optical depth at 500nm / (1) (time: 84; latitude: 192; longitude: 288)>



As you can see, the filtered object is reduced in the longitude and
latitude dimension. Let’s plot the two new objects:

.. code:: ipython3

    ax1 = od550aer_nafrica.quickplot_map('2009-3-15')
    ax2 = od550csaer_nafrica.quickplot_map('2009-3-15')



.. image:: tut00_get_started/tut00_get_started_34_0.png



.. image:: tut00_get_started/tut00_get_started_34_1.png


Filtering of time
'''''''''''''''''

Filtering of time is not yet included in the Filter class but can be
easily performed from the ``GriddedData`` object directly. If you know
the indices of the time stamps you want to crop, you can simply use
numpy indexing syntax (remember that we have a 3D array containing time,
latitude and lonfgitude).

Let’s say we want to filter the **year 2009**.

Since the time dimension corresponds the first index in the 3D data
(time, lat, lon), and since we know, that we have monthly data from
2008-2010 (see above), we may use

.. code:: ipython3

    od550aer_nafrica_2009 = od550aer_nafrica[12:24]
    od550aer_nafrica_2009.time_stamps()




.. parsed-literal::

    array(['2005-01-01T00:00:00.000000', '2005-02-01T00:00:00.000000',
           '2005-03-01T00:00:00.000000', '2005-04-01T00:00:00.000000',
           '2005-05-01T00:00:00.000000', '2005-06-01T00:00:00.000000',
           '2005-07-01T00:00:00.000000', '2005-08-01T00:00:00.000000',
           '2005-09-01T00:00:00.000000', '2005-10-01T00:00:00.000000',
           '2005-11-01T00:00:00.000000', '2005-12-01T00:00:00.000000'],
          dtype='datetime64[us]')



in order to extract the year 2009.

However, this methodology might not always be handy (imagine you have a
10 year dataset of ``3hourly`` sampled data and want to extract three
months in the 6th year …). In that case, you can perform the cropping
using the actual timestamps (for comparibility, let’s stick to 2009
here):

.. code:: ipython3

    od550aer_nafrica_2009_alt = od550aer_nafrica.crop(time_range=('1-1-2009', '1-1-2010'))
    od550aer_nafrica_2009.time_stamps()




.. parsed-literal::

    array(['2005-01-01T00:00:00.000000', '2005-02-01T00:00:00.000000',
           '2005-03-01T00:00:00.000000', '2005-04-01T00:00:00.000000',
           '2005-05-01T00:00:00.000000', '2005-06-01T00:00:00.000000',
           '2005-07-01T00:00:00.000000', '2005-08-01T00:00:00.000000',
           '2005-09-01T00:00:00.000000', '2005-10-01T00:00:00.000000',
           '2005-11-01T00:00:00.000000', '2005-12-01T00:00:00.000000'],
          dtype='datetime64[us]')



Data aggregation
''''''''''''''''

Let’s say we want to compute yearly means for each of the 3 years. In
this case we can simply call the ``downscale_time`` method:

.. code:: ipython3

    od550aer_nafrica.downscale_time('yearly')
    od550aer_nafrica.quickplot_map('2009')




.. image:: tut00_get_started/tut00_get_started_41_0.png




.. image:: tut00_get_started/tut00_get_started_41_1.png


**Note**: seasonal aggregation is not yet implemented in pyaerocom but
will follow soon.

In the following section the reading of ungridded data is illustrated
based on the example of AERONET version 3 (level 2) data. The test
dataset contains a randomly picked subset of 100 Aeronet stations.
Aeronet provides different products,

Reading of and working with ungridded data (``ReadUngridded`` and ``UngriddedData`` classes)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ungridded data in pyaerocom refers to data that is available in the form
of *files per station* and that is not sampled in a manner that it would
make sense to translate into a rgular gridded format such as the
previously introduced ``GriddedData`` class.

Data from the AERONET network (that is introduced in the following), for
instance, is provided in the form of column seperated text files per
measurement station, where columns correspond to different variables and
data rows to individual time stamps. Needless to say that the time
stamps (or the covered periods) vary from station to station.

The basic workflow for reading of ungridded data, such as Aeronet data,
is very similar to the reading of gridded data (comprising a reading
class that handles a query and returns a data class, here
`UngriddedData <http://aerocom.met.no/pyaerocom/api.html#module-pyaerocom.ungriddeddata>`__
(see also flow chart above).

Before we can continue with the data import, some things need to be said
related to the caching of ``UngriddedData`` objects.

Caching of UngriddedData
''''''''''''''''''''''''

Reading of ungridded data is often rather time-consuming. Therefore,
pyaerocom uses a caching strategy that stores loaded instances of the
``UngriddedData`` class as pickle files in a cache directory
(illustrated in the left hand side of the flowchart shown above). The
loaction of the cache directory can be accessed via:

.. code:: ipython3

    pya.const.CACHEDIR




.. parsed-literal::

    '/home/jonasg/pyaerocom/_cache/jonasg'



You may change this directory if required.

.. code:: ipython3

    print('Caching is active? {}'.format(pya.const.CACHING))


.. parsed-literal::

    Caching is active? True


**Deactivate caching**

.. code:: ipython3

    pya.const.CACHING = False

**Activate caching**

.. code:: ipython3

    pya.const.CACHING = True

**Note**: if caching is active, make sure you have enough disk quota or
change location where the files are stored.

Read Aeronet Sun v3 level 2 data
''''''''''''''''''''''''''''''''

As illustrated in the flowchart above, ungridded observation data can be
imported using the ``ReadUngridded`` class. The reading class requires
an ID for the observation network that is supposed to be read. Let’s
find the right ID for these data:

.. code:: ipython3

    pya.browse_database('Aeronet*V3*Lev2*')


.. parsed-literal::

    
    Dataset name: AeronetSunV3Lev2.daily
    Data directory: /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.daily/renamed
    Supported variables: ['od340aer', 'od440aer', 'od500aer', 'od870aer', 'ang4487aer', 'ang4487aer_calc', 'od550aer']
    Last revision: 20180820
    Reading failed for AeronetSunV3Lev2.AP. Error: OSError('Data directory /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed of observation network AeronetSunV3Lev2.AP does not exists',)
    
    Dataset name: AeronetSDAV3Lev2.daily
    Data directory: /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.SDA.V3L2.0.daily/renamed
    Supported variables: ['od500gt1aer', 'od500lt1aer', 'od500aer', 'ang4487aer', 'od550aer', 'od550gt1aer', 'od550lt1aer']
    Last revision: 20180928
    Reading failed for AeronetSDAV3Lev2.AP. Error: NetworkNotImplemented('No reading class available yet for dataset AeronetSDAV3Lev2.AP',)
    
    Dataset name: AeronetInvV3Lev2.daily
    Data directory: /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V3L2.0.daily/renamed
    Supported variables: ['abs440aer', 'angabs4487aer', 'od440aer', 'ang4487aer', 'abs550aer', 'od550aer']
    Last revision: 20180728


It found one match and the dataset ID is *AeronetSunV3Lev2.daily*. It
also tells us what variables can be loaded via the interface.

**Note**: You can safely ignore all the warnings in the output. These
are due to the fact that the testdata set does not contain all
observation networks that are available in the AEROCOM database.

.. code:: ipython3

    obs_reader = pya.io.ReadUngridded('AeronetSunV3Lev2.daily')
    print(obs_reader)


.. parsed-literal::

    
    Dataset name: AeronetSunV3Lev2.daily
    Data directory: /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.daily/renamed
    Supported variables: ['od340aer', 'od440aer', 'od500aer', 'od870aer', 'ang4487aer', 'ang4487aer_calc', 'od550aer']
    Last revision: 20180820


Let’s read the data (you can read a single or multiple variables at the
same time). For now, we only read the AOD at 550 nm:

.. code:: ipython3

    aeronet_data = obs_reader.read(vars_to_retrieve='od550aer')
    type(aeronet_data) #displays data type




.. parsed-literal::

    pyaerocom.ungriddeddata.UngriddedData



As you can see, the data object is of type ``UngriddedData``. Like the
``GriddedData`` object, also the ``UngriddedData`` class has an
informative string representation (that can be printed):

.. code:: ipython3

    print(aeronet_data)


.. parsed-literal::

    
    Pyaerocom UngriddedData
    -----------------------
    Contains networks: ['AeronetSunV3Lev2.daily']
    Contains variables: ['od550aer']
    Contains instruments: ['sun_photometer']
    Total no. of stations: 1165


Access of individual stations
'''''''''''''''''''''''''''''

.. code:: ipython3

    aeronet_data.station_name




.. parsed-literal::

    ['AOE_Baotou',
     'ARM_Ascension_Is',
     'ARM_Barnstable_MA',
     'ARM_Darwin',
     'ARM_Gan_Island',
     'ARM_Graciosa',
     'ARM_Highlands_MA',
     'ARM_HyytialaFinland',
     'ARM_Manacapuru',
     'ARM_McMurdo',
     'ARM_Nainital',
     'ARM_Oliktok_AK',
     'ARM_WAIS',
     'ATHENS-NOA',
     'Abisko',
     'Abracos_Hill',
     'Abu_Al_Bukhoosh',
     'Abu_Dhabi',
     'Adelaide_Site_7',
     'AgiaMarina_Xyliatou',
     'Agoufou',
     'Agri_School',
     'Aguas_Emendadas',
     'Aguascalientes',
     'Ahi_De_Cara',
     'Ahmedabad',
     'Aire_Adour',
     'Al_Ain',
     'Al_Dhafra',
     'Al_Khaznah',
     'Al_Qlaa',
     'Albergue_UGR',
     'Alboran',
     'Albuquerque',
     'Alishan',
     'Alta_Floresta',
     'Amazon_ATTO_Tower',
     'American_Samoa',
     'Ames',
     'Amsterdam_Island',
     'Andenes',
     'Andros_Island',
     'Angiola',
     'Anmyon',
     'AntarcticaDomeC',
     'Appalachian_State',
     'Appledore_Island',
     'Apra_Harbor',
     'Aras_de_los_Olmos',
     'Arcachon',
     'Arica',
     'Ariquiums',
     'Arizona',
     'Armilla',
     'Ascension_Island',
     'Asia1',
     'Aubiere_LAMP',
     'Autilla',
     'Avignon',
     'Azores',
     'BMKG_GAW_PALU',
     'BONDVILLE',
     'BORDEAUX',
     'BSRN_BAO_Boulder',
     'Bac_Giang',
     'Bac_Lieu',
     'Bach_Long_Vy',
     'BackGarden_GZ',
     'Badajoz',
     'Baengnyeong',
     'Bahrain',
     'Bakersfield',
     'Balbina',
     'Bambey-ISRA',
     'Bamboo',
     'Bandung',
     'Baneasa',
     'Banizoumbou',
     'Barbados',
     'Barbados_SALTRACE',
     'Barcelona',
     'Bareilly',
     'Bari_University',
     'Barnaul',
     'Barrow',
     'Baskin',
     'Bayfordbury',
     'Beijing-CAMS',
     'Beijing',
     'Beijing_RADI',
     'Belsk',
     'Belterra',
     'Ben_McDhui',
     'Ben_Salem',
     'Berlin_FUB',
     'Bermuda',
     'Bethlehem',
     'Bhola',
     'Biarritz',
     'Bidi_Bahn',
     'Big_Meadows',
     'Billerica',
     'Birdsville',
     'Birkenes',
     'Black_Forest_AMF',
     'Blida',
     'Blyth_NOAH',
     'Bodele',
     'Bolzano',
     'Bonanza',
     'Bonanza_Creek',
     'Bondoukoui',
     'Bordj_Badji_Mokhtar',
     'Bordman',
     'Bose_Institute',
     'Boulder',
     'Boyd_County_MS',
     'Bozeman',
     'Bragansa',
     'Brasilia',
     'Bratts_Lake',
     'Brisbane-Uni_of_QLD',
     'Brno_Airport',
     'Brookhaven',
     'Brussels',
     'Bucarest',
     'Bucharest_Inoe',
     'Buena_Vista',
     'Buesum',
     'Bujumbura',
     'Bure_OPE',
     'Burjassot',
     'Burtonsville',
     'Bushland',
     'CAMPO_VERDE',
     'CANDLE_LAKE',
     'CARTEL',
     'CART_SITE',
     'CASLEO',
     'CATUC_Bamenda',
     'CBBT',
     'CCNY',
     'CEILAP-BA',
     'CEILAP-Bariloche',
     'CEILAP-Comodoro',
     'CEILAP-Neuquen',
     'CEILAP-RG',
     'CEILAP-UTN',
     'CLUJ_UBB',
     'COVE',
     'COVE_SEAPRISM',
     'CRPSM_Malindi',
     'CRYSTAL_FACE',
     'CUIABA-MIRANDA',
     'CUT-TEPAK',
     'Cabauw',
     'Cabo_Raso',
     'Cabo_da_Roca',
     'Caceres',
     'Cagliari',
     'Cairo_EMA',
     'Cairo_EMA_2',
     'Cairo_University',
     'CalTech',
     'Caldwell_Parish_HS',
     'Calern_OCA',
     'Calhau',
     'Calipso_Bowers_Rd',
     'Calipso_Brookview',
     'Calipso_Carthage',
     'Calipso_Church_H_Rd',
     'Calipso_Church_Hill',
     'Calipso_Crouse_Mill',
     'Calipso_Dean_Rd',
     'Calipso_Flat_Iron',
     'Calipso_Harrison_Rd',
     'Calipso_Hillsboro',
     'Calipso_Hillsboro_E',
     'Calipso_Hurlock',
     'Calipso_Kennedyvill',
     'Calipso_Kinchaloe',
     'Calipso_Loudon_Rd',
     'Calipso_Mardela_Spr',
     'Calipso_Morgnec_Rd',
     'Calipso_NUFerry_Rd',
     'Calipso_Ninetown_Rd',
     'Calipso_Ormand_MS',
     'Calipso_Peckman_Frm',
     'Calipso_Perryville',
     'Calipso_Pine_Cove',
     'Calipso_Price',
     'Calipso_Princess_An',
     'Calipso_Prt_Deposit',
     'Calipso_Ridgely',
     'Calipso_Sabine_Frst',
     'Calipso_Sanders_ES',
     'Calipso_Sterling_PO',
     'Calipso_Strasburg',
     'Calipso_Tuckahoe',
     'Calipso_Vienna',
     'Calipso_W_Mardela',
     'Calipso_W_Strasburg',
     'Calipso_Washtn_High',
     'Calipso_West_Denton',
     'Calipso_Westfield_H',
     'Calipso_White_Marsh',
     'Calipso_WillistonLk',
     'Calipso_WofDenton',
     'Calipso_Zion',
     'Camaguey',
     'Camborne_MO',
     'Campo_Grande',
     'Campo_Grande_SONDA',
     'Canberra',
     'Cap_d_En_Font',
     'Cape_Romain',
     'Cape_San_Juan',
     'Capo_Verde',
     'Carloforte',
     'Carlsbad',
     'Carpentras',
     'CART_SITE',
     'Cat_Spring',
     'Cerro_Poyos',
     'Chao_Jou',
     'Chapada',
     'Chapais',
     'Chebogue_Point',
     'Chen-Kung_Univ',
     'Chequamegon',
     'Chiang_Mai',
     'Chiang_Mai_Met_Sta',
     'Chiayi',
     'Chiba_University',
     'Chilbolton',
     'China_Lake',
     'Chinhae',
     'Chulalongkorn',
     'Churchill',
     'City_GZ',
     'Clermont_Ferrand',
     'Coconut_Island',
     'Cold_Lake',
     'Coleambally',
     'Columbia_SC',
     'Concepcion',
     'Corcoran',
     'Cordoba-CETT',
     'Cork_UCC',
     'Coruna',
     'Creteil',
     'Crozet_Island',
     'Cuiaba',
     'DMN_Maine_Soroa',
     'DRAGON_ABERD',
     'DRAGON_ANNEA',
     'DRAGON_ARNCC',
     'DRAGON_ARNLS',
     'DRAGON_Aldine',
     'DRAGON_Aldino',
     'DRAGON_Anmyeon',
     'DRAGON_Arvin',
     'DRAGON_Aurora_East',
     'DRAGON_BATMR',
     'DRAGON_BLDND',
     'DRAGON_BLLRT',
     'DRAGON_BLTCC',
     'DRAGON_BLTIM',
     'DRAGON_BLTNR',
     'DRAGON_BOWEM',
     'DRAGON_BTMDL',
     'DRAGON_Bainbridge',
     'DRAGON_Bakersfield',
     'DRAGON_BelAir',
     'DRAGON_Beltsville',
     'DRAGON_Bokjeong',
     'DRAGON_Boulder',
     'DRAGON_CHASE',
     'DRAGON_CLLGP',
     'DRAGON_CLRST',
     'DRAGON_CPSDN',
     'DRAGON_CTNVL',
     'DRAGON_Channel_View',
     'DRAGON_Chatfield_Pk',
     'DRAGON_Clinton',
     'DRAGON_Clovis',
     'DRAGON_Conroe',
     'DRAGON_Corcoran',
     'DRAGON_Deer_Park',
     'DRAGON_DenverLaCasa',
     'DRAGON_Drummond',
     'DRAGON_EDCMS',
     'DRAGON_ELLCT',
     'DRAGON_EaglePoint',
     'DRAGON_Edgewood',
     'DRAGON_Essex',
     'DRAGON_FLLST',
     'DRAGON_FairHill',
     'DRAGON_Fort_Collins',
     'DRAGON_Fukue',
     'DRAGON_Fukue_2',
     'DRAGON_Fukue_3',
     'DRAGON_Fukuoka',
     'DRAGON_Galveston',
     'DRAGON_Galveston_DP',
     'DRAGON_GangneungWNU',
     'DRAGON_Garland',
     'DRAGON_Guwol',
     'DRAGON_Gwangju_GIST',
     'DRAGON_Hanford',
     'DRAGON_Hankuk_UFS',
     'DRAGON_Henties_1',
     'DRAGON_Henties_2',
     'DRAGON_Henties_3',
     'DRAGON_Henties_4',
     'DRAGON_Henties_5',
     'DRAGON_Henties_6',
     'DRAGON_Huron',
     'DRAGON_Jalan_ChainF',
     'DRAGON_KampungBharu',
     'DRAGON_KentIsland',
     'DRAGON_Kobe',
     'DRAGON_Kohriyama',
     'DRAGON_Kongju_NU',
     'DRAGON_Konkuk_Univ',
     'DRAGON_Korea_Univ',
     'DRAGON_Kunsan_NU',
     'DRAGON_Kyoto',
     'DRAGON_Kyungil_Univ',
     'DRAGON_LAREL',
     'DRAGON_LAUMD',
     'DRAGON_MNKTN',
     'DRAGON_Madera_City',
     'DRAGON_ManvelCroix',
     'DRAGON_Matsue',
     'DRAGON_Mokpo_NU',
     'DRAGON_Mt_Ikoma',
     'DRAGON_Mt_Rokko',
     'DRAGON_NIER',
     'DRAGON_NREL-Golden',
     'DRAGON_NW_Harris_CO',
     'DRAGON_Nara',
     'DRAGON_Nishiharima',
     'DRAGON_Niwot_Ridge',
     'DRAGON_OLNES',
     'DRAGON_ONNGS',
     'DRAGON_Osaka-North',
     'DRAGON_Osaka-South',
     'DRAGON_Osaka_Center',
     'DRAGON_PATUX',
     'DRAGON_Padonia',
     'DRAGON_Pandan_Resrv',
     'DRAGON_Parlier',
     'DRAGON_Pasadena',
     'DRAGON_PayaTerubong',
     'DRAGON_Permatang_DL',
     'DRAGON_PineyOrchard',
     'DRAGON_Platteville',
     'DRAGON_Pondok_Upeh',
     'DRAGON_Porterville',
     'DRAGON_Pusan_NU',
     'DRAGON_Pylesville',
     'DRAGON_RCKMD',
     'DRAGON_Rocky_Flats',
     'DRAGON_SHADY',
     'DRAGON_SPBRK',
     'DRAGON_Sanggye',
     'DRAGON_SeabrookPark',
     'DRAGON_Shafter',
     'DRAGON_Sinjeong',
     'DRAGON_Smith_Point',
     'DRAGON_Soha',
     'DRAGON_St_Johns_Is',
     'DRAGON_TKMPR',
     'DRAGON_Temasek_Poly',
     'DRAGON_Tranquility',
     'DRAGON_Tsukuba',
     'DRAGON_UH_Sugarland',
     'DRAGON_UH_W_Liberty',
     'DRAGON_UMRLB',
     'DRAGON_UiTM',
     'DRAGON_Visalia',
     'DRAGON_WSTFD',
     'DRAGON_Welch',
     'DRAGON_Weld_Co_Twr',
     'DRAGON_West_Houston',
     'DRAGON_WileyFord',
     'DRAGON_Worton',
     'DRAGON_Yishun_ITE',
     'Dahkla',
     'Dakar',
     'Dalanzadgad',
     'Dalma',
     'Darwin',
     'Davos',
     'Dayton',
     'Dead_Sea',
     'Denver_LaCasa',
     'Dhabi',
     'Dhadnah',
     'Dhaka_University',
     'DigitalGlobe_Cal',
     'Dilar',
     'Djougou',
     'Doi_Ang_Khang',
     'Dolly_Sods',
     'Donetsk',
     'Dongsha_Island',
     'Douliu',
     'Dry_Tortugas',
     'Dunedin',
     'Dunhuang',
     'Dunhuang_LZU',
     'Dunkerque',
     'Durban_UKZN',
     'Dushanbe',
     'EOPACE1',
     'EOPACE2',
     'EPA-NCU',
     'EPA-Res_Triangle_Pk',
     'ETNA',
     'EVK2-CNR',
     'EastMalling_MO',
     'Easton-MDE',
     'Easton_Airport',
     'Edinburgh',
     'Eforie',
     'Egbert',
     'Egbert_X',
     'Eilat',
     'El_Arenosillo',
     'El_Farafra',
     'El_Nido_Airport',
     'El_Segundo',
     'Elandsfontein',
     'Ellington_Field',
     'Epanomi',
     'Ersa',
     'Etosha_Pan',
     'Evora',
     'Exeter_MO',
     'FLIN_FLON',
     'FORTH_CRETE',
     'FZJ-JOYCE',
     'Farmington_RSVP',
     'Finokalia-FKL',
     'Fontainebleau',
     'Fort_McKay',
     'Fort_McMurray',
     'Fowlers_Gap',
     'Frenchman_Flat',
     'Fresno',
     'Fresno_2',
     'Fresno_X',
     'Frioul',
     'Fuguei_Cape',
     'Fukue',
     'Fukuoka',
     'GISS',
     'GORDO_rest',
     'GOT_Seaprism',
     'GSFC',
     'Gageocho_Station',
     'Gainesville_Airport',
     'Gaithersburg',
     'Galata_Platform',
     'Gandhi_College',
     'Gangneung_WNU',
     'Georgia_Tech',
     'Glasgow_MO',
     'Gloria',
     'Gobabeb',
     'Goldstone',
     'Gorongosa',
     'Gosan_SNU',
     'Gotland',
     'Gozo',
     'Graciosa',
     'Granada',
     'Grand_Forks',
     'Guadeloup',
     'Gual_Pahari',
     'Guam',
     'Gustav_Dalen_Tower',
     'Gwangju_GIST',
     'HESS',
     'HJAndrews',
     'HOPE-Hambach',
     'HOPE-Inselhombroich',
     'HOPE-Krauthausen',
     'HOPE-Melpitz',
     'HOPE-RWTH-Aachen',
     'Hada_El-Sham',
     'Hagerstown',
     'Halifax',
     'Hamburg',
     'Hamim',
     'Hampton_Roads',
     'Hampton_University',
     'Hangzhou-ZFU',
     'Hangzhou_City',
     'Hankuk_UFS',
     'Harvard_Forest',
     'Hefei',
     'Helgoland',
     'Helsinki',
     'Helsinki_Lighthouse',
     'Heng-Chun',
     'Henties_Bay',
     'Hermosillo',
     'Hetauda',
     'HohenpeissenbergDWD',
     'Hokkaido_University',
     'Homburi',
     'Hong_Kong_Hok_Tsui',
     'Hong_Kong_PolyU',
     'Hong_Kong_Sheung',
     'Honolulu',
     'Hornsund',
     'Howland',
     'Hua_Hin',
     'Huancayo-IGP',
     'Huelva',
     'Hyytiala',
     'IAOCA-KRSU',
     'IASBS',
     'ICIPE-Mbita',
     'IER_Cinzana',
     'IHOP-Homestead',
     'IIT_KGP_EXT_Kolkata',
     'IMAA_Potenza',
     'IMC_Oristano',
     'IMPROVE-MammothCave',
     'IMS-METU-ERDEMLI',
     'ISDGM_CNR',
     'Iasi_LOASL',
     'Ieodo_Station',
     'Ilorin',
     'Inhaca',
     'Inner_Mongolia',
     'Iqaluit',
     'Irkutsk',
     'Ispra',
     'Issyk-Kul',
     'Itajuba',
     'Ittoqqortoormiit',
     'Izana',
     'Jabal_Hafeet',
     'Jabiru',
     'Jaipur',
     'JamTown',
     'Jambi',
     'James_Res_Center',
     'Jaru_Reserve',
     'Ji_Parana',
     'Ji_Parana_SE',
     'Ji_Parana_UNIR',
     'Jingtai',
     'Joberg',
     'Jomsom',
     'JonesERC',
     'Jug_Bay',
     'KAUST_Campus',
     'KIOST_Ansan',
     'KITcube_Masada',
     'KITcube_Save',
     'KONZA_EDC',
     'KORUS_Baeksa',
     'KORUS_Daegwallyeong',
     'KORUS_Iksan',
     'KORUS_Kyungpook_NU',
     'KORUS_Mokpo_NU',
     'KORUS_NIER',
     'KORUS_Olympic_Park',
     'KORUS_Songchon',
     'KORUS_Taehwa',
     'KORUS_UNIST_Ulsan',
     'Kaashidhoo',
     'Kaiping',
     'Kandahar',
     'Kangerlussuaq',
     'Kanpur',
     'Kanzelhohe_Obs',
     'Kaoma',
     'Kapoho',
     'Karachi',
     'Karlsruhe',
     'Karunya_University',
     'Kathmandu-Bode',
     'Kathmandu_Univ',
     'Katibougou',
     'Kejimkujik',
     'Kellogg_LTER',
     'Kelowna_UAS',
     'Key_Biscayne',
     'Key_Biscayne2',
     'Kibale',
     'Kirtland_AFB',
     'Kitt-Peak_MP',
     'Kobe',
     'Koforidua_ANUC',
     'Kolimbari',
     'Konza',
     'Korea_University',
     'Krasnoyarsk',
     'Kuching',
     'Kuopio',
     'Kuujjuarapik',
     'Kuwait_Airport',
     'Kuwait_Inst_Sci_Res',
     'Kuwait_University',
     'Kyiv-AO',
     'Kyiv',
     'Kyungil_University',
     'LAMTO-STATION',
     'LAQUILA_Coppito',
     'LISCO',
     'LMOS_Zion_Site',
     'LOS_FIEROS_98',
     'LSU',
     'LW-SCAN',
     'La_Crau',
     'La_Jolla',
     'La_Laguna',
     'La_Parguera',
     'La_Paz',
     'Laegeren',
     'Lahore',
     'Lake_Argyle',
     'Lake_Erie',
     'Lake_Lefroy',
     'Lamezia_Terme',
     'Lampedusa',
     'Lan_Yu_Island',
     'Lanai',
     'Langtang',
     'Lannion',
     'Lanzhou_City',
     'Las_Galletas',
     'Le_Fauga',
     'Lecce_University',
     'Leicester',
     'Leipzig',
     'Leland_HS',
     'Lerwick_MO',
     'Liangning',
     'Lille',
     'Lingshan_Mountain',
     'Litang',
     'Lochiel',
     'Loftus_MO',
     'London-UCL-UAO',
     'Longyearbyen',
     'Los_Alamos',
     'Los_Fieros',
     'Loskop_Dam',
     'Luang_Namtha',
     'Lubango',
     'Lucinda',
     'Lugansk',
     'Lulin',
     'Lumbini',
     'Lunar_Lake',
     'MAARCO',
     'MALE',
     'MCO-Hanimaadhoo',
     'MD_Science_Center',
     'MISR-JPL',
     'MPI_Mainz',
     'MVCO',
     'Mace_Head',
     'Madison',
     'Madrid',
     'Maeson',
     'Maggie_Valley',
     'Magurele_Inoe',
     'Mainz',
     'Makassar',
     'Malaga',
     'Mammoth_Lake',
     'Manaus',
     'Manaus_EMBRAPA',
     'Manila_Observatory',
     'Manus',
     'Marambio',
     'Marbella_San_Pedro',
     'Maricopa',
     'Marina',
     'Marseille',
     'Martova',
     'Masdar_Institute',
     'Maun_Tower',
     'Mauna_Loa',
     'McClellan_AFB',
     'McMurdo',
     'Medellin',
     'Medenine-IRA',
     'Melpitz',
     'Merredin',
     'Mesa_Lakes',
     'Messina',
     'MetObs_Lindenberg',
     'Mexico_City',
     'Mezaira',
     'Miami',
     'Midway_Island',
     'Milyering',
     'Mingo',
     'Minqin',
     'Minsk',
     'Misamfu',
     'Missoula',
     'Mobile_C_050608',
     'Mobile_C_060708',
     'Mobile_DDun_051308W',
     'Mobile_Kanpur_East',
     'Mobile_Kanpur_SE',
     'Mobile_Kanpur_South',
     'Mobile_Kanpur_W2',
     'Mobile_Kanpur_West',
     'Mobile_N_050608',
     'Mobile_N_051308W',
     'Mobile_N_051508E',
     'Mobile_N_052908W',
     'Mobile_N_053108E',
     'Mobile_N_060708',
     'Mobile_N_061408W',
     'Mobile_S_011509_ND',
     'Mobile_S_050608',
     'Mobile_S_051308W',
     'Mobile_S_051508E',
     'Mobile_S_052908W',
     'Mobile_S_060708',
     'Mobile_S_062308',
     'Modena',
     'Modesto',
     'Moldova',
     'Monclova',
     'Mongu',
     'Mongu_Inn',
     'Mont_Joli',
     'Monterey',
     'Montesoro_Bastia',
     'Montsec',
     'Moscow_MSU_MO',
     'Moss_Landing',
     'Mount_Chacaltaya',
     'Mount_Wilson',
     'Mukdahan',
     'Munich_Maisach',
     'Munich_University',
     'Murcia',
     'Muscat',
     'Mussafa',
     'Muztagh_Ata',
     'Mwinilunga',
     'Myanmar',
     'NAM_CO',
     'NASA_Ames',
     'NASA_KSC',
     'NASA_LaRC',
     'NCU_Taiwan',
     'ND_Marbel_Univ',
     'NEON-Boulder',
     'NEON-CPER',
     'NEON-Disney',
     'NEON-HQ',
     'NEON-SoaprootSaddle',
     'NEON17-SJER',
     'NEON_Bartlett',
     'NEON_CLBJ',
     'NEON_CVALLA',
     'NEON_DEJU',
     'NEON_GRSM',
     'NEON_GUAN',
     'NEON_GrandJunction',
     'NEON_HEAL',
     'NEON_Harvard',
     'NEON_HarvardForest',
     'NEON_HighParkFire',
     'NEON_Ivanpah',
     'NEON_KONZ',
     'NEON_LENO',
     'NEON_MLBS',
     'NEON_MOAB',
     'NEON_OAES',
     'NEON_ONAQ',
     'NEON_ORNL',
     'NEON_OSBS',
     'NEON_RMNP',
     'NEON_SCBI',
     'NEON_SERC',
     'NEON_Sterling',
     'NEON_TALL',
     'NEON_TOOL',
     'NEON_UKFS',
     'NEON_UNDE',
     'NEON_WOOD',
     'NEW_YORK',
     'NGHIA_DO',
     'NSA_YJP_BOREAS',
     'NUIST',
     'NW_Chapel_Hill',
     'Nainital',
     'Nairobi',
     'Namibe',
     'Napoli_CeSMA',
     'Nara',
     'Narsarsuaq',
     'Natal',
     'Nauru',
     'Ndola',
     'Nes_Ziona',
     'New_Delhi',
     'New_Hampshire_Univ',
     'NhaTrang',
     'Niabrara',
     'Niamey',
     'Nicelli_Airport',
     'Nicosia',
     'Niigata',
     'Nong_Khai',
     'Norfolk_State_Univ',
     'North_Pole',
     'Noto',
     'Noumea',
     'Nouragues',
     'Ny_Alesund',
     'OBERNAI',
     'OBS-SSA',
     'OHP_OBSERVATOIRE',
     'OK_St_Univ',
     'OPAL',
     'ORS_Hermosillo',
     'ORS_UNAM_ISNP',
     'OkefenokeeNWR',
     'Okinawa',
     'Omkoi',
     'Oostende',
     'Ordway-Swisher',
     'Orizaba',
     'Orlean_Bricy',
     'Osaka-North',
     'Osaka',
     'Ouagadougou',
     'Ouarzazate',
     'Oujda',
     'Oukaimeden',
     'Owens_Lake',
     'Oxford',
     'Oyster',
     'PEARL',
     'PKU_PEK',
     'PNNL',
     'POLWET_Rzecin',
     'PRINCE_ALBERT',
     'Paardefontein',
     'Paddockwood',
     'Pafos',
     'Pagosa_Springs',
     'Palaiseau',
     'Palangkaraya',
     'Palencia',
     'Palgrunden',
     'Palma_de_Mallorca',
     'Panama_BCI',
     'Pantanal',
     'Pantnagar',
     'Paposo',
     'Paracou',
     'Paris',
     'Park_Brasilia',
     'Penn_State_Univ',
     'Perth',
     'Peterhof',
     'Petrolina_SONDA',
     'Philadelphia',
     'Pic_du_midi',
     'Pickle_Lake',
     'Pietersburg',
     'Pimai',
     'Pitres',
     'Pokhara',
     'Pontianak',
     'Poprad-Ganovce',
     'Porquerolles',
     'Portglenone_MO',
     'Porto_Nacional',
     'Porto_Velho',
     'Porto_Velho_UNIR',
     'Possession_Island',
     'Potchefstroom',
     'Potosi_Mine',
     'Praia',
     'Pretoria_CSIR-DPSS',
     'Progress',
     'Prospect_Hill',
     'Puerto_Madryn',
     'Puli',
     'Pullman',
     'Pune',
     'Pusan_NU',
     'Puspiptek',
     'QOMS_CAS',
     'Qiandaohu',
     'Quarzazate',
     'Quito_USFQ',
     'REUNION_ST_DENIS',
     'Raciborz',
     'Ragged_Point',
     'Railroad_Valley',
     'Rame_Head',
     'Ras_El_Ain',
     'Realtor',
     'Red_Bluff',
     'Red_Mountain_Pass',
     'Red_River_Delta',
     'Resolute_Bay',
     'Rexburg_Idaho',
     'Rhyl_MO',
     'Richland',
     'Rimrock',
     'Rio_Branco',
     'Rio_Piedras',
     'Rio_de_Janeiro_UFRJ',
     'Rogers_Dry_Lake',
     'Rome_ESA_ESRIN',
     'Rome_La_Sapienza',
     'Rome_Tor_Vergata',
     'Roosevelt_Roads',
     'Rossfeld',
     'Rottnest_Island',
     'SACOL',
     'SAGRES',
     'SANTA_CRUZ',
     'SANTA_CRUZ_UTEPSA',
     'SDU1',
     'SDU2',
     'SDU3',
     'SDU4',
     'SEARCH-Centreville',
     'SEARCH-Centreville2',
     'SEARCH-OLF',
     'SEARCH-Yorkville',
     'SEDE_BOKER',
     'SEGC_Lope_Gabon',
     'SERC',
     'SKUKUZA_AEROPORT',
     'SMART',
     'SMART_POL',
     'SMEX',
     'SMHI',
     'SP-EACH',
     'SP_Bayboro',
     'SSA_YJP_BOREAS',
     'SS_OJP_BOREAS',
     'Saada',
     'Sable_Island',
     'Saih_Salam',
     'Saint_Mandrier',
     'Salon_de_Provence',
     'San_Giuliano',
     'San_Nicolas',
     'San_Nicolas_Vandal',
     'San_Pietro_Capo',
     'Sandia_NM_PSEL',
     'Santa_Cruz_Tenerife',
     'Santa_Monica_Colg',
     'Santarem',
     'Santiago',
     'Santiago_Beauchef',
     'Sao_Martinho_SONDA',
     'Sao_Paulo',
     'Saturn_Island',
     'Senanga',
     'Seoul_SNU',
     'Sesheke',
     'Sevastopol',
     'Sevilleta',
     'Seysses',
     'Shagaya_Park',
     'Shelton',
     'Shirahama',
     'Shouxian',
     'Sigma_Space_Corp',
     'Silpakorn_Univ',
     'Simonstown_IMT',
     'Singapore',
     'Sinhgad',
     'Sioux_Falls',
     'Sioux_Falls_X',
     'Sir_Bu_Nuair',
     'Sirmione_Museo_GC',
     'Skukuza',
     'Smith_Island_CBF',
     'Socheongcho',
     'Sodankyla',
     'Solar_Village',
     'Solwezi',
     'Son_La',
     ...]



Let’s say you are interested in the city of Leipzig, Germany.

.. code:: ipython3

    station_data = aeronet_data['Leipzig']
    type(station_data)




.. parsed-literal::

    pyaerocom.stationdata.StationData



As you can see, the returned object is of type ``StationData``, which is
one further data format of pyaerocom (note that this is not displayed in
the simplified flowchart above). ``StationData`` may be useful for
individual stations and is an extended Python dictionary (if you are
familiar with Python).

You may print it to see what is in there:

.. code:: ipython3

    print(station_data)


.. parsed-literal::

    
    Pyaerocom StationData
    ---------------------
    instrument_name: sun_photometer
    unit (<class 'pyaerocom._lowlevel_helpers.BrowseDict'>)
    dataset_name: AeronetSunV3Lev2.daily
    station_name: Leipzig
    PI: Brent_Holben
    stat_lat: nan
    stat_lon: nan
    stat_alt: nan
    ts_type_src: daily
    od550aer: 2001-05-20 12:00:00    0.190538
    2001-05-21 12:00:00    0.165246
    2001-05-22 12:00:00    0.117999
    2001-05-23 12:00:00    0.067452
    2001-05-24 12:00:00    0.077793
    2001-05-30 12:00:00    0.119798
    2001-06-03 12:00:00    0.121039
    2001-06-06 12:00:00    0.312110
    2001-06-07 12:00:00    0.192976
    2001-06-09 12:00:00    0.558903
    2001-06-11 12:00:00    0.206287
    2001-06-12 12:00:00    0.294526
    2001-06-13 12:00:00    0.333145
    2001-06-14 12:00:00    0.346363
    2001-06-15 12:00:00    0.332472
    2001-06-16 12:00:00    0.220668
    2001-06-17 12:00:00    0.103815
    2001-06-19 12:00:00    0.146963
    2001-06-20 12:00:00    0.149631
    2001-06-21 12:00:00    0.322529
    2001-06-23 12:00:00    0.266764
    2001-06-24 12:00:00    0.148060
    2001-06-25 12:00:00    0.468637
    2001-06-26 12:00:00    0.168430
    2001-06-27 12:00:00    0.224706
    2001-06-28 12:00:00    0.837737
    2001-06-29 12:00:00    0.472877
    2001-06-30 12:00:00    0.421142
    2001-07-01 12:00:00    0.285850
    2001-07-02 12:00:00    0.149566
                             ...   
    2017-09-20 12:00:00    0.098478
    2017-09-21 12:00:00    0.285237
    2017-09-22 12:00:00    0.296735
    2017-09-23 12:00:00    0.350108
    2017-09-27 12:00:00    0.336902
    2017-09-28 12:00:00    0.253596
    2017-09-29 12:00:00    0.172088
    2017-09-30 12:00:00    0.173876
    2017-10-12 12:00:00    0.076930
    2017-10-14 12:00:00    0.067515
    2017-10-15 12:00:00    0.039083
    2017-10-16 12:00:00    0.174384
    2017-10-17 12:00:00    0.087807
    2017-10-18 12:00:00    0.178155
    2017-10-19 12:00:00    0.116929
    2017-10-22 12:00:00    0.065865
    2017-10-29 12:00:00    0.124535
    2017-10-30 12:00:00    0.041524
    2017-11-02 12:00:00    0.143081
    2017-11-03 12:00:00    0.158916
    2017-11-06 12:00:00    0.110552
    2017-11-17 12:00:00    0.081437
    2017-11-24 12:00:00    0.055906
    2017-11-26 12:00:00    0.101109
    2017-11-27 12:00:00    0.073161
    2017-11-29 12:00:00    0.063464
    2017-11-30 12:00:00    0.135819
    2017-12-01 12:00:00    0.160344
    2017-12-03 12:00:00    0.109541
    2017-12-07 12:00:00    0.087100
    Length: 2713, dtype: float64
    dtime (array, 2713 items)
       [numpy.datetime64('2001-05-20T12:00:00')
        numpy.datetime64('2001-05-21T12:00:00')
        ...
        numpy.datetime64('2017-12-03T12:00:00')
        numpy.datetime64('2017-12-07T12:00:00')]
    
    Data coordinates
    .................
    latitude: 51.352500000000006
    longitude: 12.435278
    altitude: 125.0


As you can see, this station contains a time-series of the AOD at 550
nm. If you like, you can plot this time-series:

.. code:: ipython3

    station_data.plot_variable('od550aer', style=' xg', figsize=(16,6)).set_title('Leipzig AOD all times')




.. parsed-literal::

    Text(0.5,1,'Leipzig AOD all times')




.. image:: tut00_get_started/tut00_get_started_70_1.png


You can also retrieve the ``StationData`` with specifying more
constraints using ``to_station_data`` (e.g. in monthly resolution and
only for the year 2010). And you can overlay different curves, by
passing the axes instance returned by the plotting method:

.. code:: ipython3

    ax=aeronet_data.to_station_data('Leipzig', 
                                    start=2010, 
                                    freq='daily').plot_variable('od550aer', 
                                                                label='daily')
    
    ax=aeronet_data.to_station_data('Leipzig', 
                                    start=2010, 
                                    freq='monthly').plot_variable('od550aer', 
                                                                  label='monthly',
                                                                  ax=ax)
    ax.legend()
    ax.set_title('Leipzig AODs 2010')




.. parsed-literal::

    Text(0.5,1,'Leipzig AODs 2010')




.. image:: tut00_get_started/tut00_get_started_72_1.png


You can also plot the time-series directly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For instance, if you want to do an air-quality check for you next
bouldering trip, you may call:

.. code:: ipython3

    aeronet_data.plot_station_timeseries('Fontainebleau', 'od550aer', ts_type='monthly',
                                         start=2006).set_title('AOD in Fontainebleau, 2006')




.. parsed-literal::

    Text(0.5,1,'AOD in Fontainebleau, 2006')




.. image:: tut00_get_started/tut00_get_started_74_1.png


Seems like November is a good time (maybe a bit rainy though)

Colocation of model and obsdata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have different data objects loaded we can continue with
colocation. In the following, both the all-sky and the clear-sky data
from CAM53-Oslo will be colocated with the subset of Aeronet stations
that we just loaded.

The colocation will be performed for the year of 2010 and two scatter
plots will be created.

You have also the option to apply a certain filter when colocating using
a valid filter name. Here, we use global data and exclude mountain
sides.

.. code:: ipython3

    col_all_sky_glob = pya.colocation.colocate_gridded_ungridded_2D(od550aer, aeronet_data, 
                                                                    ts_type='monthly',
                                                                    start=2010,
                                                                    filter_name='WORLD-noMOUNTAINS')
    type(col_all_sky_glob)


.. parsed-literal::

    Old name of function colocate_gridded_ungridded(still works)


.. parsed-literal::

    Interpolating data of shape (12, 192, 288). This may take a while.
    Successfully interpolated cube




.. parsed-literal::

    pyaerocom.colocateddata.ColocatedData



Let’s do the same for the clear-sky data.

.. code:: ipython3

    col_clear_sky_glob = pya.colocation.colocate_gridded_ungridded_2D(od550csaer, aeronet_data, 
                                                                      ts_type='monthly',
                                                                      start=2010,
                                                                      filter_name='WORLD-noMOUNTAINS')
    type(col_clear_sky_glob)


.. parsed-literal::

    Old name of function colocate_gridded_ungridded(still works)


.. parsed-literal::

    Interpolating data of shape (12, 192, 288). This may take a while.
    Successfully interpolated cube




.. parsed-literal::

    pyaerocom.colocateddata.ColocatedData



.. code:: ipython3

    ax1 = col_all_sky_glob.plot_scatter()
    ax1.set_title('All sky (2010, monthly)')




.. parsed-literal::

    Text(0.5,1,'All sky (2010, monthly)')




.. image:: tut00_get_started/tut00_get_started_81_1.png


.. code:: ipython3

    ax2 = col_clear_sky_glob.plot_scatter()
    ax2.set_title('Clear sky (2010, monthly)')




.. parsed-literal::

    Text(0.5,1,'Clear sky (2010, monthly)')




.. image:: tut00_get_started/tut00_get_started_82_1.png


… or for EUROPE:

.. code:: ipython3

    pya.colocation.colocate_gridded_ungridded_2D(od550aer, aeronet_data,
                                                 ts_type='monthly',
                                                 start=2010,
                                                 filter_name='EUROPE-noMOUNTAINS').plot_scatter()


.. parsed-literal::

    Old name of function colocate_gridded_ungridded(still works)


.. parsed-literal::

    Interpolating data of shape (12, 192, 288). This may take a while.
    Successfully interpolated cube




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x7f3cd223cf98>




.. image:: tut00_get_started/tut00_get_started_84_3.png

