
# ==[ IMPORTS ]===========================================================
from log import LOG
from dataAccessor import DataAccessor
from dataSeries import DataSeries

from exceptions import NoNetworksFoundException
from exceptions import RssiValueTransmissionException
from exceptions import SsidLengthException

# ==[ ASSIGN PORTS ]======================================================
# --< X-Axis Motor >-----
X_MOTOR_PORTS_LIST = (16, 18, 22, 24)
X_MOTOR_MIN_DEGREE = -180
X_MOTOR_MAX_DEGREE = 180

# ==[ MAIN APPLICATION]===================================================

dataSeries = DataSeries("TestSeries")
dataAccessor = DataAccessor()

for x in range(5):
    for y in range(5):
        for retrys in range(2):
            try:
                tempListOfNetworks = dataAccessor.getDataPoint(x,y)
                dataSeries.extendNetworkList(tempListOfNetworks)
                break
            except SsidLengthException:
                LOG("======> SSID exception catched, retrys: " + str(retrys) + " <======")



        


dataSeries.printToConsole()
dataAccessor.serialPort.close()



