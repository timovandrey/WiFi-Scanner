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
# 05.03.2021 -> implemented pickle functionalities
# ========================================================================

# ==[ IMPORTS ]===========================================================
from log import LOG
from network import Network
try:
    import cPickle as pickle
except:
    import pickle

# ==[ CLASS ]=============================================================
class DataSeries:

    # ==[ CONSTANTS ]=====================================================
    DEFAULT_SCAN_TIME_IN_SECONDS = 2.5
    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, name):
        self.name = name
        self.networks = []

    # ==[ METHODS ]=======================================================
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

    # --< Pickles this object to a file >-----
    def pickle(self, filename):

        # Pickling works this way:
        # 1) Open destination file in write mode
        # 2) pickle.dump(<to be pickled obj>, <dest-file-stream>)
        # 3) Close destination filestream
        #
        # Unpickling works this way:
        # 1) Open file with pickled objects
        # 2) obj = pickle.load(<file-with-pickled-obj-stream>)
        # 3) Close file with pickled obj filestream

        LOG("Starting to pickle \"" + str(self.name) + "\".")
        LOG("Opening dumpfile \"" + str(filename) + "\".")
        try:
            outfile = open(filename, 'wb')
        except OSError:
            LOG("An error occured while opening \"" + str(filename) + "\".")

        LOG("Starting to dump data into \"" + str(filename) + "\".")
        try:
            pickle.dump(self, outfile)
        except OSError:
            LOG("An error occured while pickling \"" + str(filename) + "\".")

        try:
            outfile.close()
        except OSError:
            LOG("An error occured while closing \"" + str(filename) + "\".")

        LOG("Successfully pickled \"" + str(self.name) + "\" to \"" + str(filename) + "\".")

    # ==[ STATIC METHODS ]================================================
    # --< unpickles a file to a DataSeries object >-----
    @staticmethod
    def unpickle(filename):
        LOG("Starting to unpickle file \"" + str(filename) + "\".")
        try:
            infile = open(filename, 'rb')
        except OSError:
            LOG("An error occured while opening \"" + str(filename) + "\".")
        
        try:
            PickledDataSeries = pickle.load(infile)
        except OSError:
            LOG("An error occured while unpickling \"" + str(filename) + "\".")

        try:
            infile.close()
        except OSError:
            LOG("An error occured while closing \"" + str(filename) + "\".")

        LOG("Successfully unpickled \"" + str(PickledDataSeries.name) + "\" from \"" + str(filename) + "\".")

        return PickledDataSeries

    @staticmethod
    def getEstimatedScanTimeInMinutes(x, y):
        return ((DataSeries.DEFAULT_SCAN_TIME_IN_SECONDS * x * y) / 60)







    
