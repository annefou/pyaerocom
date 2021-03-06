def _init_logger():
    import logging
    ### LOGGING
# Note: configuration will be propagated to all child modules of
# pyaerocom, for details see 
# http://eric.themoritzfamily.com/learning-python-logging.html
    logger = logging.getLogger('pyaerocom')
    
    default_formatter = logging.Formatter(\
       "%(asctime)s:%(levelname)s:\n%(message)s")
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(default_formatter)
    
    logger.addHandler(console_handler)
    
    logger.setLevel(logging.CRITICAL)
    
    print_log = logging.getLogger('pyaerocom_print')
    
    print_handler = logging.StreamHandler()
    print_handler.setFormatter(logging.Formatter("%(message)s"))
    
    print_log.addHandler(print_handler)
    
    print_log.setLevel(logging.INFO)
    return (logger, print_log)

def change_verbosity(new_level='debug'):
    if isinstance(new_level, str):
        if not new_level in LOGLEVELS:
            raise ValueError("Invalid input for loglevel, choose "
                             "from {}".format(LOGLEVELS.keys()))
        new_level = LOGLEVELS[new_level]
    logger.setLevel(new_level)
    
### Functions for package initialisation
def _init_supplemental():
    from pkg_resources import get_distribution
    from os.path import abspath, dirname
    return (get_distribution('pyaerocom').version, abspath(dirname(__file__)))


def _init_config(package_dir):
    from socket import gethostname
    from os.path import join
    if gethostname() == 'aerocom-users-ng':
        print("Initiating global PATHS for Aerocom users server")
        cfg = join(package_dir, 'data', 'paths_user_server.ini')
    else:
        cfg = join(package_dir, 'data', 'paths.ini')
    return Config(config_file=cfg)

def check_requirements(logger):
    GEONUM_AVAILABLE = True
    BASEMAP_AVAILABLE = True
    try:
        import geonum
    except:
        GEONUM_AVAILABLE = False
        logger.warn('geonum library is not installed. Some features will not '
                    'be available (e.g. conversion of pressure to altitude')
    try:
        from mpl_toolkits.basemap import Basemap
    except:
        BASEMAP_AVAILABLE = False
        logger.warn('basemap extension library is not installed (or cannot be '
                    'imported. Some features will not be available')
    return (GEONUM_AVAILABLE, BASEMAP_AVAILABLE)

__version__, __dir__ = _init_supplemental()

logger, print_log = _init_logger()
LOGLEVELS = {'debug': 10,
             'info': 20,
             'warning': 30,
             'error': 40,
             'critical': 50}

(GEONUM_AVAILABLE, 
 BASEMAP_AVAILABLE) = check_requirements(logger)

# Imports
from . import _lowlevel_helpers
from . import obs_io
# custom toplevel classes
from .variable import Variable
from .region import Region
from .config import Config

const = _init_config(__dir__)
if not const.READY:
    logger.warning("WARNING: Failed to initiate data directories")
    
from . import mathutils
from . import multiproc
from . import vert_coords

from .vertical_profile import VerticalProfile
from .stationdata import StationData
from .griddeddata import GriddedData
from .ungriddeddata import UngriddedData
from .filter import Filter
from .colocateddata import ColocatedData
from . import colocation
from . import analysis

from . import io
from . import plot


#from .ungriddeddata import UngriddedData
from .io.helpers import search_data_dir_aerocom
from .io.utils import browse_database
from .variable import get_variable
from .utils import create_varinfo_table
#from .obsdata import ObsData, ProfileData, StationData
#print('Elapsed time init pyaerocom: {} s'.format(time()-t0))



