# ========================================================================
# Title:        Data
# Author:       Jonas Buuck, Timo Vandrey
# Date:         02.03.2021
# Description:  Class to describe all collected data.
#
# --< LOG >-----
# 01.03.2021 -> class created by Timo
# 04.03.2021 -> modification of constructor and attributes by Jonas
# ========================================================================

# ==[ IMPORTS ]===========================================================
from log import LOG
from network import network

class DataSeries:

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, name):
        self.name = name
        self.networks = []

    def extendNetworkList(self, tempListOfNetworks):

        # --< iterate over list of temporary networks >-----
        for tempNetwork in tempListOfNetworks:
            networkAlreadyContained = False

            # --< iterate over list of existing networks, check if temporary network already contained >-----
            for networkOfExistingNetworks in self.networks:

                # --< if network already contained >-----
                if (tempNetwork.ssid == networkInExistingNetworks.ssid):
                    LOG("Network already contained in List")
                    networkAlreadyContained = True

                    networkInExistingNetworks.dataPoints.append(tempNetwork.dataPoints[0])
                    break

        # --< if network not already contained, append to list of networks >-----
        if(networkAlreadyContained == False):
            self.networks.append(tempNetwork)    






    def importFromJson(jsonFilePath):
        pass

    def exportToJson(jsonFilePath):
        pass



    
