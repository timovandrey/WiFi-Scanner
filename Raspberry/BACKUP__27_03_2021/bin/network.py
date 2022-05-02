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

class Network:
    def __init__(self, ssid, arraySizeYaw, arraySizePitch):
        self.ssid = ssid
        self.dataPoints = [[0 for y in range(arraySizePitch)] for x in range(arraySizeYaw)]


    # ==[ METHODS ]=======================================================
    def printToConsole(self):
        print("SSID: " + self.ssid)
        print(self.dataPoints)
        print("\n")
        






    

    

        




