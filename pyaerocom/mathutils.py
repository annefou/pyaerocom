#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods ofcd pyaerocom
"""

import numpy as np
from pyaerocom import const, logger
from pyaerocom.variable import VarNameInfo
import iris
from cf_units import Unit
from scipy.stats import pearsonr, spearmanr, kendalltau
### LAMBDA FUNCTIONS
in_range = lambda x, low, high: low <= x <= high

### OTHER FUNCTIONS
def calc_statistics(data, ref_data, lowlim=None, highlim=None):
    """Calc statistical properties from two data arrays
    
    Calculates the following statistical properties based on the two provided
    1-dimensional data arrays and returns them in a dictionary (keys are 
    provided after the arrows):
        
        - Mean value of both arrays -> refdata_mean, data_mean
        - RMS (Root mean square) -> rms
        - NMB (Normalised mean bias), in percent-> nmb
        - MNMB (Modified normalised mean bias), in percent -> mnmb
        - FGE (Fractional gross error), in percent -> fge
        - R (Pearson correlation coefficient) -> R
        - R_spearman (Spearman corr. coeff) -> R_spearman
        
    Note
    ----
    Nans are removed from the input arrays, information about no. of removed
    points can be inferred from keys `totnum` and `success` in return dict.
    
    Parameters
    ----------
    data : ndarray
        array containing data, that is supposed to be compared with reference
        data
    ref_data : ndarray
        array containing data, that is used to compare `data` array with
    lowlim : float
        lower end of considered value range (e.g. if set 0, then all datapoints
        where either ``data`` or ``ref_data`` is smaller than 0 are removed)
    highlim : float
        upper end of considered value range
        
    Returns
    -------
    dict
        dictionary containing computed statistics    
    
    Raises
    ------
    ValueError 
        if either of the input arrays has dimension other than 1
        
    """
    data = np.asarray(data)
    ref_data = np.asarray(ref_data)
    
    if not data.ndim == 1 or not ref_data.ndim == 1:
        raise ValueError('Invalid input. Data arrays must be one dimensional')
        
    result = {}
    mask = ~np.isnan(ref_data) * ~np.isnan(data)
    
    data, ref_data = data[mask], ref_data[mask]
    if lowlim is not None:
        valid = np.logical_and(data>lowlim, ref_data>lowlim)
        data = data[valid]
        ref_data = ref_data[valid]
    if highlim is not None:
        valid = np.logical_and(data<highlim, ref_data<highlim)
        data = data[valid]
        ref_data = ref_data[valid]
    
    difference = data - ref_data
    num_points = sum(mask)
    
    result['refdata_mean'] = np.mean(ref_data)
    result['data_mean'] = np.mean(data)
    result['rms'] = np.sqrt(np.sum(np.power(difference, 2)) / num_points)
    result['nmb'] = np.sum(difference) / np.sum(ref_data)*100.
    tmp = difference / (data + ref_data)
    
    result['mnmb'] = 2. / num_points * np.sum(tmp) * 100.
    result['fge'] = 2. / num_points * np.sum(np.abs(tmp)) #* 100.
    #result['fge'] = 2. / np.sum(np.abs(tmp)) * 100.
    
    result['R'] = pearsonr(data, ref_data)[0]
    result['R_spearman'] = spearmanr(data, ref_data)[0]
    result['R_kendall'] = kendalltau(data, ref_data)[0]
    result['totnum'] = len(mask)
    result['success'] = num_points
    
    return result

def closest_index(num_array, value):
    """Returns index in number array that is closest to input value"""
    return np.argmin(np.abs(np.asarray(num_array) - value))

def numbers_in_str(input_string):
    """This method finds all numbers in a string
    
    Note
    ----
    - Beta version, please use with care
    - Detects only integer numbers, dots are ignored
    
    Parameters
    ----------
    input_string : str
        string containing numbers
    
    Returns
    -------
    list
        list of strings specifying all numbers detected in string
        
    Example
    -------
    >>> numbers_in_str('Bla42Blub100')
    [42, 100]
    """
    numbers = []
    IN_NUM=False
    c_num = None
    for char in input_string:
        try:
            int(char)
            if not IN_NUM:
                IN_NUM = True
                c_num = char
            elif IN_NUM:
                c_num += char
        except:
            if IN_NUM:
                numbers.append(c_num)
            IN_NUM=False
    if IN_NUM:
        numbers.append(c_num)
    return numbers    
    
def calc_ang4487aer(data):
    """Compute Angstrom coefficient (440-870nm) from 440 and 870 nm AODs
    
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Note
    ----
    Requires the following two variables to be available in provided data 
    object:
        
        1. od440aer
        2. od870aer
    
    Returns
    -------
    ndarray
        array containing computed angstrom coefficients
    
    Raises 
    ------
    AttributError
        if either 'od440aer' or 'od870aer' are not available in data object
    """
    if not all([x in data for x in ['od440aer','od870aer']]):
        raise AttributeError("Either of the two (or both) required variables "
                             "(od440aer, od870aer) are not available in data")
    od440aer, od870aer = data['od440aer'], data['od870aer']
    return compute_angstrom_coeff(od440aer, od870aer, .44, .87)

def calc_od550aer(data):
    """Compute AOD at 550 nm using Angstrom coefficient and 500 nm AOD
        
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    """
    return _calc_od_helper(data=data, 
                           var_name='od550aer', 
                           to_lambda=.55, 
                           od_ref='od500aer', 
                           lambda_ref=.50, 
                           od_ref_alt='od440aer', 
                           lambda_ref_alt=.44,
                           use_angstrom_coeff='ang4487aer')

def calc_abs550aer(data):
    """Compute AOD at 550 nm using Angstrom coefficient and 500 nm AOD
        
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    """
    return _calc_od_helper(data=data, 
                           var_name='abs550aer', 
                           to_lambda=.55, 
                           od_ref='abs500aer', 
                           lambda_ref=.50, 
                           od_ref_alt='abs440aer', 
                           lambda_ref_alt=.44,
                           use_angstrom_coeff='angabs4487aer')
    
def calc_od550gt1aer(data):
    """Compute coarse mode AOD at 550 nm using Angstrom coeff. and 500 nm AOD
        
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    """
    return _calc_od_helper(data=data, 
                           var_name='od550gt1aer', 
                           to_lambda=.55, 
                           od_ref='od500gt1aer', 
                           lambda_ref=.50,
                           use_angstrom_coeff='ang4487aer')

def calc_od550lt1aer(data):
    """Compute fine mode AOD at 550 nm using Angstrom coeff. and 500 nm AOD
        
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    """
    return _calc_od_helper(data=data, 
                           var_name='od550lt1aer', 
                           to_lambda=.55, 
                           od_ref='od500lt1aer', 
                           lambda_ref=.50,
                           use_angstrom_coeff='ang4487aer')
        
    
def compute_angstrom_coeff(od1, od2, lambda1, lambda2):
    """Compute Angstrom coefficient based on 2 optical densities
    
    Parameters
    ----------
    od1 : :obj:`float` or :obj:`ndarray`
        AOD at wavelength 1
    od2 : :obj:`float` or :obj:`ndarray`
        AOD at wavelength 2
    lambda1 : :obj:`float` or :obj:`ndarray`
        wavelength 1
    lambda 2 : :obj:`float` or :obj:`ndarray`
        wavelength 2
        
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        Angstrom exponent(s)
    """
    return -np.log(od1 / od2) / np.log(lambda1 / lambda2)

def compute_angstrom_coeff_cubes(od1, od2, lambda1=None, lambda2=None):
    """Compute Angstrom coefficient cube based on 2 optical densitiy cubes
    
    Parameters
    ----------
    od1 : iris.cube.Cube
        AOD at wavelength 1
    od2 : iris.cube.Cube
        AOD at wavelength 2
    lambda1 : float
        wavelength 1
    lambda 2 : float
        wavelength 2
        
    Returns
    -------
    Cube
        Cube containing Angstrom exponent(s)
    """
    from pyaerocom import GriddedData
    if isinstance(od1, GriddedData):
        od1 = od1.grid
    if isinstance(od2, GriddedData):
        od2 = od2.grid
    if lambda1 is None:
        lambda1 = VarNameInfo(od1.var_name).wavelength_nm
    if lambda2 is None:
        lambda2 = VarNameInfo(od2.var_name).wavelength_nm
    
    if not od1.shape == od2.shape:
        raise ValueError('Input grids do not have the same shape')
    
    logr = iris.analysis.maths.log(od1 / od2)
    
    wvl_r = np.log(lambda1 / lambda2)
    ang = -1*iris.analysis.maths.divide(logr, wvl_r)
    ang.units = Unit(1)
    return ang

def compute_od_from_angstromexp(to_lambda, od_ref, lambda_ref, 
                                 angstrom_coeff):
    """Compute AOD at specified wavelength 
    
    Uses Angstrom coefficient and reference AOD to compute the 
    corresponding wavelength shifted AOD
    
    Parameters
    ----------
    to_lambda : :obj:`float` or :obj:`ndarray`
        wavelength for which AOD is calculated
    od_ref : :obj:`float` or :obj:`ndarray`
        reference AOD
    lambda_ref : :obj:`float` or :obj:`ndarray`
        wavelength corresponding to reference AOD
    angstrom_coeff : :obj:`float` or :obj:`ndarray`
        Angstrom coefficient
        
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    
    """
    return od_ref * (lambda_ref / to_lambda) ** angstrom_coeff

def _calc_od_helper(data, var_name, to_lambda, od_ref, lambda_ref, 
                    od_ref_alt=None, lambda_ref_alt=None, 
                    use_angstrom_coeff='ang4487aer'):
    """Helper method for computing ODs
    
    Parameters
    ----------
    data : dict-like
        data object containing loaded results used to compute the ODs at a new
        wavelength
    var_name : str
        name of variable that is supposed to be computed (is used in order to 
        see whether a global lower threshold is defined for this variable and
        if this is the case, all computed values that are below this threshold
        are replaced with NaNs)
    to_lambda : float
        wavelength of computed AOD
    od_ref : :obj:`float` or :obj:`ndarray`
        reference AOD
    lambda_ref : :obj:`float` or :obj:`ndarray`
        wavelength corresponding to reference AOD
    od_ref_alt : :obj:`float` or :obj:`ndarray`, optional
        alternative reference AOD (is used for datapoints where former is 
        invalid)
    lambda_ref_alt : :obj:`float` or :obj:`ndarray`, optional
        wavelength corresponding to alternative reference AOD
    use_angstrom_coeff : str
        name of Angstrom coefficient in data, that is used for computation
        
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
        
    Raises
    ------
    AttributeError
        if neither ``od_ref`` nor ``od_ref_alt`` are available in data, or if
        ``use_angstrom_coeff`` is missing
    """
    if not od_ref in data:
        logger.warning('Reference OD at {} nm is not available in data, '
                       'checking alternative'.format(lambda_ref))
        if od_ref_alt is None or not od_ref_alt in data:
            raise AttributeError('No alternative OD found for computation of '
                                 '{}'.format(var_name))
        return compute_od_from_angstromexp(to_lambda=to_lambda, 
                                           od_ref=data[od_ref_alt],
                                           lambda_ref=lambda_ref_alt, 
                                           angstrom_coeff=data[use_angstrom_coeff])
    elif not use_angstrom_coeff in data:
        raise AttributeError("Angstrom coefficient (440-870 nm) is not "
                             "available in provided data")
    result = compute_od_from_angstromexp(to_lambda=to_lambda, 
                                          od_ref=data[od_ref],
                                          lambda_ref=lambda_ref, 
                                          angstrom_coeff=data[use_angstrom_coeff])
    # optional if available
    if od_ref_alt in data:
        # fill up time steps that are nans with values calculated from the
        # alternative wavelength to minimise gaps in the time series
        mask = np.argwhere(np.isnan(result))
        
        if len(mask) > 0: #there are nans
            ods_alt = data[od_ref_alt][mask]
            ang = data[use_angstrom_coeff][mask]
            replace = compute_od_from_angstromexp(to_lambda=to_lambda, 
                                                    od_ref=ods_alt,
                                                    lambda_ref=lambda_ref_alt, 
                                                    angstrom_coeff=ang)
            result[mask] = replace
    
    try:
        # now replace all values with NaNs that are below the global lower threshold
        below_thresh = result < const.VAR_PARAM[var_name]['minimum']
        result[below_thresh] = np.nan
    except:
        logger.warn("Could not access lower limit from global settings for "
                    "variable {}".format(var_name))
    
    return result

def exponent(num):
    """Get exponent of input number
        
    Parameters
    ----------
    num : :obj:`float` or iterable
        input number
    
    Returns
    -------
    :obj:`int` or :obj:`ndarray` containing ints
        exponent of input number(s)
        
    Example
    -------
    >>> from pyaerocom.mathutils import exponent
    >>> exponent(2340)
    3
    """
    return np.floor(np.log10(abs(np.asarray(num)))).astype(int)

def range_magnitude(low, high):
    """Returns magnitude of value range
    
    Parameters
    ----------
    low : float
        lower end of range
    high : float
        upper end of range
    
    Returns
    -------
    int
        magnitudes spanned by input numbers
    
    Example
    -------
    
    >>> range_magnitude(0.1, 100)
    3
    >>> range_magnitude(100, 0.1)
    -3
    >>> range_magnitude(1e-3, 1e6)
    9
    
    """
    return exponent(high) - exponent(low)

if __name__ == "__main__":
    #import doctest
    exp = exponent(23)
    print(numbers_in_str('Bla42Blub100'))
    #run tests in all docstrings
    #doctest.testmod()
    
    