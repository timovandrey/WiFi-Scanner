class NoNetworksFoundException(Exception):
    pass
class RssiValueTransmissionException(Exception):
    pass
class SsidLengthException(Exception):
    pass
class MotorOutOfLimitsException(Exception):
    pass
class DataSeriesIsNullException(Exception):
    pass
class DataSeriesIsNotOfTypeDataSeriesException(Exception):
    pass
class NoDataSeriesExistentException(Exception):
    pass
class CouldntPickleException(Exception):
    pass
class CouldntUnPickleException(Exception):
    pass
class CouldntExportException(Exception):
    pass
class FileNonExistentException(Exception):
    pass
class FileNotValidException(Exception):
    pass
class CouldntOpenFileException(Exception):
    pass