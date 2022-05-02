
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

PICKLE_FILE = "bigDatSeries.pickle"
SIMULATED_X_STEPS = 20
SIMULATED_Y_STEPS = 20

# ==[ MAIN APPLICATION ]===================================================

dataSeries = DataSeries("TestSeries", 0, 3, 3, 3, 3)
dataAccessor = DataAccessor()

errors = 0

for x in range(dataSeries.stepsToScanYaw):
    for y in range(dataSeries.stepsToScanPitch):
        for retrys in range(4):
            try:
                LOG("Currently requesting:\t[" + str(x) + "][" + str(y) + "]")
                dataAccessor.addDataPoint(x, y, dataSeries)
                break
            except SsidLengthException:
                LOG("======> SSID exception catched, retrys: " + str(retrys) + " <======")
                errors += 1
            except RssiValueTransmissionException as e:
                LOG("======> RSSI exception catched, retrys: " + str(retrys) + " message" + str(e) + " <======")
                errors += 1
            except NoNetworksFoundException:
                LOG("======> Network not found exception catched, retrys: " + str(retrys) + " <======")
                errors += 1

LOG("== ERRORS: " + str(errors))


dataSeries.printToConsole()
dataAccessor.serialPort.close()

dataSeries.pickle(PICKLE_FILE)
unpickledDataSeries = DataSeries.unpickle(PICKLE_FILE)
print("Unpickled Data:\n")
unpickledDataSeries.printToConsole()



