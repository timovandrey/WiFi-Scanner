
# ==[ IMPORTS ]===========================================================
from log import LOG
from dataAccessor import DataAccessor
from dataSeries import DataSeries
from antennaFiniteStateMachine import *

from exceptions import NoNetworksFoundException
from exceptions import RssiValueTransmissionException
from exceptions import SsidLengthException


stateMachine = AntennaFiniteStateMachine()
dataSeries = DataSeries("Test Series", -3, 3, 3, 1, 1)
stateMachine.IStartScan = True
stateMachine.IDataSeries = dataSeries

while True:
    stateMachine.run()

