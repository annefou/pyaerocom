#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""

# TODO: Docstrings
import pytest
import numpy.testing as npt
from pandas import Timestamp
from pyaerocom.test.settings import TEST_RTOL
from pyaerocom.io.readgridded import ReadGridded

@pytest.fixture(scope='module')
def dataset():
    '''Read ECMWF data between 2003 and 2008
    '''
    return ReadGridded(name="ECMWF_CAMS_REAN",
                       start="1-1-2003",
                       stop="31-12-2007")
    
def test_variables(dataset):
    npt.assert_array_equal(dataset.vars,
                           ['ang4487aer', 'od440aer', 'od550aer', 'od550bc', 
                            'od550dust', 'od550oa', 'od550so4', 'od550ss', 
                            'od865aer'])
    
def test_years_available(dataset):
    npt.assert_array_equal(dataset.years,
                           [ 2003,
                             2004,
                             2005,
                             2006,
                             2007,
                             2008,
                             2009,
                             2010,
                             2011,
                             2012,
                             2013,
                             2014,
                             2015,
                             2016,
                             9999])    

    
def test_meta(dataset):
    npt.assert_array_equal([len(dataset.files),
                            dataset.data_dir,
                            dataset._start, 
                            dataset._stop,
                            list(dataset.get_years_to_load())],
                            [190,
                             '/lustre/storeA/project/aerocom/aerocom-users-database/ECMWF/ECMWF_CAMS_REAN/renamed',
                             Timestamp("1-1-2003"), 
                             Timestamp("31-12-2007"),
                             [2003, 2004, 2005, 2006, 2007]])
    
def test_read_var(dataset):
    from numpy import datetime64
    d = dataset.read_var(var_name="od550aer", ts_type="daily")
    npt.assert_array_equal([d.var_name, sum(d.shape), d.start, d.stop],
                           ["od550aer", 1826 + 161 + 320,
                            datetime64('2003-01-01T00:00:00.000000'),
                            datetime64('2007-12-31T00:00:00.000000')])
    vals = [d.longitude.points[0],
            d.longitude.points[-1],
            d.latitude.points[0],
            d.latitude.points[-1],
            d[0].mean()]
    nominal = [-180.0, 178.875, 90.0, -90.0, 0.08924646]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    return d

def test_read_vars(dataset):
    d = dataset.read(['od440aer', 'od550aer', 'od865aer'], 
                           ts_type="daily")
    
    
    vals = [len(d),
            sum(d[0].shape),
            sum(d[1].shape),
            sum(d[2].shape)]
    nominal = [3, 2307, 2307, 2307]
    npt.assert_array_equal(vals, nominal)
    
    vals = [d[0][1825].mean(), d[1][1825].mean(), d[2][1825].mean()]
    nominal = [0.11754113, 0.09734518, 0.06728536]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    return d
    
if __name__=="__main__":
    d = dataset()
    test_variables(d)
    test_years_available(d)
    test_meta(d)
    test_read_var(d)
    
    dat = test_read_vars(d)