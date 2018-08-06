################################################################
# read_aeronet_invv3.py
#
# read Aeronet inversion V3 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180802 by Jonas Gliss for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA

import os

import numpy as np
import pandas as pd

from pyaerocom import const
from pyaerocom.mathutils import calc_abs550aer, calc_od550aer
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom import StationData

class ReadAeronetInvV3(ReadAeronetBase):
    """Interface for reading Aeronet inversion V3 Level 1.5 and 2.0 data

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined 
        in ``SUPPORTED_DATASETS``
    """
    #: Mask for identifying datafiles 
    _FILEMASK = '*.all'
    
    #: version log of this class (for caching)
    __version__ = "0.01"
    
    #: Name of dataset (OBS_ID)
    DATASET_NAME = const.AERONET_INV_V3L2_DAILY_NAME
    
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.AERONET_INV_V3L2_DAILY_NAME,
                          const.AERONET_INV_V3L15_DAILY_NAME]
    
    #: default variables for read method
    DEFAULT_VARS = ['abs550aer',
                    'od550aer']
    
    #: value corresponding to invalid measurement
    NAN_VAL = -999.
    
    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {'abs550aer'     :   ['abs440aer',
                                         'angabs4487aer'],
                    'od550aer'     :   ['od440aer',
                                        'ang4487aer']}
                    
    #: Functions that are used to compute additional variables (i.e. one 
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'abs550aer'     :   calc_abs550aer,
                'od550aer'      :   calc_od550aer}
    
    #: dictionary specifying the file column names (values) for each Aerocom 
    #: variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['abs440aer'] = 'Absorption_AOD[440nm]'
    VAR_NAMES_FILE['angabs4487aer'] = 'Absorption_Angstrom_Exponent_440-870nm'
    VAR_NAMES_FILE['od440aer'] = 'AOD_Extinction-Total[440nm]'
    VAR_NAMES_FILE['ang4487aer'] = 'Extinction_Angstrom_Exponent_440-870nm-Total'
    
    #: dictionary specifying the file column names (values) for each 
    #: metadata key (cf. attributes of :class:`StationData`, e.g.
    #: 'station_name', 'longitude', 'latitude', 'altitude')
    META_NAMES_FILE = {}
    #META_NAMES_FILE['data_quality_level'] = 'DATA_TYPE'
    META_NAMES_FILE['date'] = 'Date(dd:mm:yyyy)'
    META_NAMES_FILE['time'] = 'Time(hh:mm:ss)'
    META_NAMES_FILE['day_of_year'] = 'Day_of_Year(fraction)'
    META_NAMES_FILE['station_name'] = 'Site'
    META_NAMES_FILE['stat_lat'] = 'Latitude(Degrees)'
    META_NAMES_FILE['stat_lon'] = 'Longitude(Degrees)'
    META_NAMES_FILE['stat_alt'] = 'Elevation(m)'
    
    #: List of variables that are provided by this dataset (will be extended 
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())

    # TODO: currently every file is read, regardless of whether it actually
    # contains the desired variables or not. Do we need that? Slows stuff down..
    # Also: Quick check reading all files in the database showed that only 
    # about 20% of the files contain the default variables..
    def read_file(self, filename, vars_to_retrieve=None,
                  vars_as_series=False):
        """Read Aeronet file containing results from v2 inversion algorithm

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : list
            list of str with variable names to read
        vars_as_series : bool
            if True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects
            
        Returns
        -------
        StationData
            dict-like object containing results
        

        Example
        -------
        >>> import pyaerocom.io as pio
        >>> obj = pio.read_aeronet_invv2.ReadAeronetInvV2()
        >>> files = obj.get_file_list()
        >>> filedata = obj.read_file(files[0])
        """
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
       
        #create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        
        # create empty arrays for meta information
        for item in self.META_NAMES_FILE:
            data_out[item] = []
            
        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            data_out[var] = []
        
        # Iterate over the lines of the file
        self.logger.debug("Reading file {}".format(filename))
    
        with open(filename, 'rt') as in_file:

            data_out['dataset_info'] = in_file.readline().strip()
            self.logger.debug('Skipping line: {}'.format(in_file.readline()))
            data_out['algorithm_info'] = in_file.readline().strip()
            
            self.logger.debug('Skipping line: {}'.format(in_file.readline()))
            
            
            c_dummy = in_file.readline().strip().split(',')
            data_out['freq_info'] = c_dummy[0].strip()
            
            pi_info = c_dummy[1].strip().split(';')
            # re.split(r'=|\,',c_dummy)
            
            
            data_out['PI'] = pi_info[0].split('PI=')[1].strip()
            data_out['PI_email'] = pi_info[1].split('PI Email=')[1].strip()

            #skip next two lines
            self.logger.debug('Skipping line:\n{}'.format(in_file.readline()))
            #self.logger.info('Skipping line:\n{}'.format(in_file.readline()))
            
            col_index_str = in_file.readline()
            if col_index_str != self._last_col_index_str:
                self.logger.debug("Header has changed, reloading col_index map")
                self._update_col_index(col_index_str)
            col_index = self.col_index
            
            # dependent on the station, some of the required input variables
            # may not be provided in the data file. These will be ignored
            # in the following list that iterates over all data rows and will
            # be filled below, with vectors containing NaNs after the file 
            # reading loop
            vars_available = {}
            for var in vars_to_read:
                if var in col_index:
                    vars_available[var] = col_index[var]
                else:
                    self.logger.warning("Variable {} not available in file {}"
                                        .format(var, os.path.basename(filename)))
                
            for line in in_file:
                # process line
                dummy_arr = line.strip().split(self.COL_DELIM)

                # This uses the numpy datestring64 functions that i.e. also 
                # support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[col_index['date']].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[col_index['time']]])
                datestring = '+'.join([datestring, '00:00'])
                data_out['dtime'].append(np.datetime64(datestring))
                
                for var in self.META_NAMES_FILE:
                    val = dummy_arr[col_index[var]]
                    try:
                        # e.g. lon, lat, altitude
                        val = float(val)
                    except:
                        pass
                    data_out[var].append(val)

                # copy the data fields that are available (rest will be filled
                # below)
                for var, idx in vars_available.items():
                    val = np.float_(dummy_arr[idx])
                    if val == self.NAN_VAL: 
                        val = np.nan
                    data_out[var].append(val)
        
        # convert all lists to numpy arrays
        data_out['dtime'] = np.asarray(data_out['dtime'])
        
        for item in self.META_NAMES_FILE:
            data_out[item] = np.asarray(data_out[item])
            
        for var in vars_to_read:
            if var in vars_available:
                array = np.asarray(data_out[var])
            else:
                array = np.zeros(len(data_out['dtime'])) * np.nan
            data_out[var] = array
        
        # compute additional variables (if applicable)
        data_out = self.compute_additional_vars(data_out, vars_to_compute)
        
        if vars_as_series:        
            for var in (vars_to_read + vars_to_compute):
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var], 
                                              index=data_out['dtime'])
                else:
                    del data_out[var]
            
        return data_out

if __name__=="__main__":
    from pyaerocom import change_verbosity
    change_verbosity('critical')
    read = ReadAeronetInvV3()
    read15 = ReadAeronetInvV3(const.AERONET_INV_V3L15_DAILY_NAME)
    read.verbosity_level = 'info'
    
    data = read.read_first_file()
    data15 = read15.read_first_file()
    print(data)
    #print(data15)
    #read.print_all_columns()
    
    #ax = data.plot_variable('od550aer')
    
    #all_lvl2 = read.read()