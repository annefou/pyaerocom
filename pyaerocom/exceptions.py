#Copyright (C) 2017 met.no
#Norwegian Meteorological Institute
#Box 43 Blindern
#0313 OSLO
#NORWAY
#E-mail: jan.griesfeller@met.no, jonas.gliss@met.no
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA

"""
Module containing pyaerocom custom exceptions
"""
class AerocomConnectionError(IOError):
    pass

class ColocationError(ValueError):
    pass

class CoordinateError(ValueError):
    pass

class CoordinateNameError(CoordinateError):
    pass

class DataCoverageError(ValueError):
    pass

class DataDimensionError(ValueError):
    pass

class DataUnitError(ValueError):
    pass

class DimensionOrderError(DataDimensionError):
    pass

class NDimError(DataDimensionError):
    pass

class DataExtractionError(ValueError):
    pass

class EbasFileError(ValueError):
    pass

class FileConventionError(IOError):
    pass

class IllegalArgumentError(ValueError):
    pass

class LongitudeConstraintError(ValueError):
    pass

class MetaDataError(AttributeError):
    pass

class NetworkNotSupported(NotImplementedError):
    pass

class NetworkNotImplemented(NotImplementedError):
    pass

class NetcdfError(IOError):
    pass

class NotInFileError(IOError):
    pass

class TimeZoneError(AttributeError):
    pass

class TimeMatchError(AttributeError):
    pass

class TemporalResolutionError(ValueError):
    pass

class VarNotAvailableError(DataCoverageError):
    pass

class VariableDefinitionError(IOError):
    pass

class VariableNotFoundError(IOError):
    pass

class YearNotAvailableError(DataCoverageError):
    pass