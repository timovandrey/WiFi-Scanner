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
    def __init__(self, ssid, dataPoints):
        self.ssid = ssid
        self.dataPoints = dataPoints


    # ==[ METHODS ]=======================================================
    def printToConsole(self):
        print("\tSSID: " + self.ssid)

        for tempDataPoint in self.dataPoints:
            print("\t\t" + str(tempDataPoint))    

        print("\n")

    # ==[ STATIC METHODS ]================================================
    @staticmethod
    def checkListOfNetworks(listOfNetworks):
        # --< compare every network in list with every network in list >-----
        for tempNetwork1 in listOfNetworks:
            for tempNetwork2 in listOfNetworks:

                # --< if SSID is equal but RSSI is not , remove network with lower rssi >-----
                if((tempNetwork1.ssid == tempNetwork2.ssid) and (tempNetwork1.dataPoints[0].rssi != tempNetwork2.datapoints[0].rssi)):
                    if(tempNetwork1.dataPoints[0].rssi <= tempNetwork2.dataPoints[0].rssi):
                        listOfNetworks.remove(tempNetwork1)
                    else:
                        listOfNetworks.remove(tempNetwork2)
                    






    

    

        




