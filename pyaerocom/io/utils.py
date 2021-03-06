#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level I/O utility methods for pyaerocom
"""

from pyaerocom.io.aerocom_browser import AerocomBrowser
from pyaerocom.io.readgridded import ReadGridded
from pyaerocom.io.readungridded import ReadUngridded
from pyaerocom import const, change_verbosity

def browse_database(model_or_obs, verbose=False):
    """Browse Aerocom database using model or obs ID (or wildcard)
    
    Searches database for matches and prints information about all matches 
    found (e.g. available variables, years, etc.)
    
    Parameters
    ----------
    model_or_obs : str
        model or obs ID or search pattern 
    verbose : bool
        if True, verbosity level will be set to debug, else to critical
        
    Example
    -------
    >>> import pyaerocom as pya
    >>> pya.io.browse_database('AATSR*ORAC*v4*')
    Pyaerocom ReadGridded
    ---------------------
    Model ID: AATSR_ORAC_v4.01
    Data directory: /lustre/storeA/project/aerocom/aerocom-users-database/CCI-Aerosol/CCI_AEROSOL_Phase2/AATSR_ORAC_v4.01/renamed
    Available variables: ['abs550aer', 'ang4487aer', 'clt', 'landseamask', 'od550aer', 'od550dust', 'od550gt1aer', 'od550lt1aer', 'pixelcount']
    Available years: [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
    Available time resolutions ['daily']
    """
    if not verbose:
        change_verbosity('critical')
    else:
        change_verbosity('debug')
    browser = AerocomBrowser()
    matches = browser.find_matches(model_or_obs)
    if len(matches) is 0:
        print('No match could be found for {}'.format(model_or_obs))
        return
    elif len(matches) > 20:
        print('Found more than 20 matches for based on input string {}:\n\n'
              'Matches: {}\n\n'
              'To receive more detailed information, please specify search ID '
              'more accurately'.format(model_or_obs, matches))
        return
    for match in matches:
        try:
            if match in const.OBS_IDS:
                reader = ReadUngridded(match)
            else:
                reader = ReadGridded(match)
            print(reader)
        except Exception as e:
            print('Reading failed for {}. Error: {}'.format(match,
                  repr(e)))
    

if __name__=='__main__':
    
    obs_id = 'AATSR*'
    
    browse_database('AATSR_SU*')
    
    browse_database('AATSR*ORAC*v4*')
    
    browse_database(obs_id)