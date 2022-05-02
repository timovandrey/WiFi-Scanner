
# ==[ IMPORTS ]===========================================================
from log import LOG
from dataAccessor import DataAccessor



# ==[ ASSIGN PORTS ]======================================================
# --< X-Axis Motor >-----
X_MOTOR_PORTS_LIST = (16, 18, 22, 24)
X_MOTOR_MIN_DEGREE = -180
X_MOTOR_MAX_DEGREE = 180

# ==[ MAIN APPLICATION]===================================================

dataSeries = DataSeries("TestSeries")
dataAccessor = DataAccessor()

tempListOfNetworks = dataAccessor.getDataPoint(0,0)

dataSeries.extendNetworkList(tempListOfNetworks)



