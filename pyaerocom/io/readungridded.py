#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################
# readoddata.py
#
# observational data reading class
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171024 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2017 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no, jonas.gliss@met.no
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
import os, logging

from pyaerocom.exceptions import NetworkNotImplemented, NetworkNotSupported
from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSdaV2
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
from pyaerocom.io.read_aeronet_invv2 import ReadAeronetInvV2
from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3
from pyaerocom.io.read_aeronet_sunv2 import ReadAeronetSunV2
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.io.read_earlinet import ReadEarlinet
from pyaerocom.io.read_ebas import ReadEbas

from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from pyaerocom.ungriddeddata import UngriddedData

from pyaerocom import const, print_log

# TODO Note: Removed infiles (list of files from which datasets were read, since it 
# was not used anywhere so far)
class ReadUngridded(object):
    """Factory class for reading of ungridded data based on obsnetwork ID"""
    SUPPORTED = [ReadAeronetInvV3,
                 ReadAeronetInvV2,
                 ReadAeronetSdaV2,
                 ReadAeronetSdaV3,
                 ReadAeronetSunV2,
                 ReadAeronetSunV3,
                 ReadEarlinet,
                 ReadEbas]
    
    # when this file exists, an existing cache file is not read
    _DONOTCACHEFILE = os.path.join(const.OBSDATACACHEDIR, 'DONOTCACHE')

    def __init__(self, datasets_to_read=const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
                 vars_to_retrieve=None, ignore_cache=False):
        
        #will be assigned in setter method of dataset_to_read
        self._datasets_to_read = []
        #: dictionary containing reading classes for each dataset to read (will
        #: be filled in setter of datasets_to_read)
        self._readers = {}
        
        self.data = None
        
        self.datasets_to_read = datasets_to_read
    
        # optional: list of variables that are supposed to be imported, if 
        # None, all variables provided by the corresponding network are loaded
        self.vars_to_retrieve = vars_to_retrieve
        
        self.revision = {}
        self.data_version = {}
    
        self.cache_files = {}
        
        # initiate a logger for this class
        self.logger = logging.getLogger(__name__)
        
        if ignore_cache:
            self.logger.info('Deactivating caching')
            const.CACHING = False
            
    @property
    def ignore_cache(self):
        if os.path.exists(self._DONOTCACHEFILE) or not const.CACHING:
            return True
        return False
    
    @property
    def datasets_to_read(self):
        """List of datasets supposed to be read"""
        return self._datasets_to_read
    
    @datasets_to_read.setter
    def datasets_to_read(self, datasets):
        if isinstance(datasets, str):
            datasets = [datasets]
        elif not isinstance(datasets, (tuple, list)):
            raise IOError('Invalid input for parameter datasets_to_read')
        for ds in datasets:
            self.find_read_class(ds)
            
        self._datasets_to_read = datasets    
    
    def dataset_provides_variables(self, dataset_to_read):
        """List of variables provided by a certain dataset"""
        if dataset_to_read in self._readers:
            return self._readers[dataset_to_read].PROVIDES_VARIABLES
        return self.find_read_class(dataset_to_read).PROVIDES_VARIABLES
      
    def get_reader(self, dataset_to_read):
        """Helper method that returns loaded reader class
        
        Parameters
        -----------
        dataset_to_read : str
            Name of dataset
        
        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base 
            class :class:`ReadUngriddedBase`)
        
        Raises
        ------
        NetworkNotSupported
            if network is not supported by pyaerocom
        NetworkNotImplemented
            if network is supported but no reading routine is implemented yet
        """
        if not dataset_to_read in self._readers:
            self.find_read_class(dataset_to_read)
        return self._readers[dataset_to_read]
    
    def find_read_class(self, dataset_to_read):
        """Find reading class for dataset name
        
        Loops over all reading classes available in :attr:`SUPPORTED` and finds
        the first one that matches the input dataset name, by checking the 
        attribute :attr:`SUPPORTED_DATASETS` in each respective reading class
        
        Parameters
        -----------
        dataset_to_read : str
            Name of dataset
        
        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base 
            class :class:`ReadUngriddedBase`)
        
        Raises
        ------
        NetworkNotSupported
            if network is not supported by pyaerocom
        NetworkNotImplemented
            if network is supported but no reading routine is implemented yet
        
        """
        if dataset_to_read in self._readers:
            return self._readers[dataset_to_read]
        if not dataset_to_read in const.OBS_IDS:
            raise NetworkNotSupported("Network {} is not supported"
                                      .format(dataset_to_read))
        for cls in self.SUPPORTED:
            if dataset_to_read in cls.SUPPORTED_DATASETS:
                self._readers[dataset_to_read] = cls(dataset_to_read)
                return self._readers[dataset_to_read]
        raise NetworkNotImplemented("No reading class available yet for dataset "
                                    "{}".format(dataset_to_read))
        
    def __str__(self):
        #raise NotImplementedError("Requires review after API changes")
        s=''
        for ds in self.datasets_to_read:
            s += '\n{}'.format(self.get_reader(ds))
        return s
        
    def read_dataset(self, dataset_to_read, vars_to_retrieve=None, **kwargs):
        """Read single dataset into instance of :class:`ReadUngridded`
        
        Note
        ----
        This method does not write class attribute :attr:`data` (only
        :func:`read` does)
        
        Parameters
        ----------
        dataset_to_read : str
            name of dataset
        vars_to_retrieve : list
            list of variables to be retrieved. If None (default), the default
            variables of each reading routine are imported
            
        Returns
        --------
        UngriddedData
            data object
        """
        if vars_to_retrieve is None:
            # Note: self.vars_to_retrieve may be None as well, then
            # default variables of each network are read
            vars_to_retrieve = self.vars_to_retrieve 
            
        reader = self.get_reader(dataset_to_read)
        
        if vars_to_retrieve is None:
            vars_to_retrieve = reader.PROVIDES_VARIABLES
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
            
        # Since this interface enables to load multiple datasets, each of 
        # which support a number of variables, here, only the variables are 
        # considered that are supported by the dataset
        vars_available = [var for var in vars_to_retrieve if var in 
                          reader.PROVIDES_VARIABLES]
        
        # read the data sets
        cache_hit_flag = False
        
        if not self.ignore_cache:
            # initate cache handler
            cache = CacheHandlerUngridded(reader, vars_available, **kwargs)
            if cache.check_and_load():
                all_avail = True
                for var in vars_available:
                    if not var in cache.loaded_data:
                        all_avail = False
                        break
                if all_avail:
                    self.logger.info('Found Cache match for {}'.format(dataset_to_read))
                    cache_hit_flag = True
                    data = cache.loaded_data
            
        if not cache_hit_flag:
            self.logger.info('No Cache match found for {}. Reading from files (this '
                        'may take a while)'.format(dataset_to_read))
            _loglevel = print_log.level
            print_log.setLevel(logging.INFO)
            data = reader.read(vars_available, **kwargs)
            print_log.setLevel(_loglevel)
        self.revision[dataset_to_read] = reader.data_revision
        self.data_version[dataset_to_read] = reader.__version__
        
        # write the cache file
        if not cache_hit_flag and not self.ignore_cache:
            cache.write(data)
        
        return data
    
    def read(self, datasets_to_read=None, vars_to_retrieve=None,
             **kwargs):
        """Read observations

        Iter over all datasets in :attr:`datasets_to_read`, call 
        :func:`read_dataset` and append to data object
        
        Example
        -------
        >>> import pyaerocom.io.readungridded as pio
        >>> from pyaerocom import const
        >>> obj = pio.ReadUngridded(dataset_to_read=const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME)
        >>> obj.read()
        >>> print(obj)
        >>> print(obj.metadata[0.]['latitude'])
        """
        if datasets_to_read is not None:
            self.datasets_to_read = datasets_to_read
        if vars_to_retrieve is not None:
            self.vars_to_retrieve = vars_to_retrieve
            
        data = UngriddedData()
        for ds in self.datasets_to_read:
            self.logger.info('Reading {} data'.format(ds))
            data.append(self.read_dataset(ds, vars_to_retrieve, **kwargs))
            self.logger.info('Successfully imported {} data'.format(ds))
        self.data = data
        return data
    
    @property
    def SUPPORTED_DATASETS(self):
        """Returns list of strings containing all supported dataset names"""
        l = []
        for r in self.SUPPORTED:
            l.extend(r.SUPPORTED_DATASETS)
        return l 
    
    @property
    def supported_datasets(self):
        return self.SUPPORTED_DATASETS
    
if __name__=="__main__":

    reader = ReadUngridded(ignore_cache=True)
    
    data = reader.read([const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
                        const.AERONET_SUN_V3L2_AOD_DAILY_NAME], 
                    vars_to_retrieve='od550aer', 
                    last_file=10)
    
    
    
    