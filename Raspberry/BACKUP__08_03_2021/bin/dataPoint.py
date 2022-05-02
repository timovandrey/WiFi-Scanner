# ========================================================================
# Title:        DataPoint
# Author:       Jonas Buuck
# Date:         04.03.2021
# Description:  Class to describe a dataPoint
#
# --< LOG >-----
# 04.03.2021 -> class created by Jonas
# 05.03.2021 -> __string__ added
# ========================================================================

# ==[ CLASS ]=============================================================
class DataPoint:

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, x, y, rssi):
        self.x = x
        self.y = y
        self.rssi = rssi

    # ==[ METHODS ]=======================================================
    # --< toString >-----
    def __str__(self):
        return ("@[" + str(self.x) + "][" + str(self.y) + "] : " + str(self.rssi) + " dBm")