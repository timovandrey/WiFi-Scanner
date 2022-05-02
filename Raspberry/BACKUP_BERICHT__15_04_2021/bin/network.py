# ========================================================================
# Title:        Network
# Author:       Jonas Buuck, Timo Vandrey
# Date:         02.03.2021
# Description:  Class to describe fetched network SSI values from antenna.
#
# --< LOG >-----
# 01.03.2021 -> class created by Jonas
# 04.03.2021 -> modification of constructor, addDataPoint method implemented
# ========================================================================

import copy

class Network:
    def __init__(self, ssid, arraySizeYaw, arraySizePitch):
        self.ssid = ssid
        self.dataPoints = [[0 for y in range(arraySizePitch)] for x in range(arraySizeYaw)]


    # ==[ METHODS ]=======================================================
    def printToConsole(self):
        print("SSID: " + self.ssid)
        print(self.dataPoints)
        print("\n")

    # Returns the corresponding mW-Value for the input dBm-Value
    @staticmethod
    def dBmToMuW(dbm_val):
        return (10 ** (dbm_val/10)) * 10**3

    @staticmethod
    def dataPointsDbmToMw(dataPoints):
        dataPointsInMw = copy.deepcopy(dataPoints)

        for x in range(len(dataPoints)):
            for y in range(len(dataPoints[x])):
                dataPointsInMw[x][y] = Network.dBmToMuW(dataPoints[x][y])
        
        return dataPointsInMw        

        






    

    

        




