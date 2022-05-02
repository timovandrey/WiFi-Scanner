# ========================================================================
# Title:        Data
# Author:       Jonas Buuck, Timo Vandrey
# Date:         02.03.2021
# Description:  Class to describe all collected data.
#
# --< LOG >-----
# 01.03.2021 -> class created by Timo
# 04.03.2021 -> modification of constructor and attributes by Jonas
# 05.03.2021 -> implementing toString function
# ========================================================================

# ==[ IMPORTS ]===========================================================
from log import LOG
from network import Network

class DataSeries:

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, name):
        self.name = name
        self.networks = []

    def printToConsole(self):

        # --< print header and name of data series >-----
        print("====================================================================")
        print("Name of dataseries: " + self.name)
        print("List of Networks:")

        # --< print list of networks >-----
        for tempNetwork in self.networks:
            tempNetwork.printToConsole()
            
        print("====================================================================")

    def extendNetworkList(self, tempListOfNetworks):

        # --< iterate over list of temporary networks >-----
        for tempNetwork in tempListOfNetworks:
            networkAlreadyContained = False

            # --< iterate over list of existing networks, check if temporary network already contained >-----
            for networkInExistingNetworks in self.networks:

                # --< if network already contained >-----
                if (tempNetwork.ssid == networkInExistingNetworks.ssid):
                    LOG("Network \"" + tempNetwork.ssid + "\" already in list, adding data to network heatmap")
                    networkAlreadyContained = True

                    networkInExistingNetworks.dataPoints.append(tempNetwork.dataPoints[0])
                    break

            # --< if network not already contained, append to list of networks >-----
            if(networkAlreadyContained == False):
              LOG("Network \"" + tempNetwork.ssid + "\" not in list, appending now")
              self.networks.append(tempNetwork)    

    def pickle():





    
