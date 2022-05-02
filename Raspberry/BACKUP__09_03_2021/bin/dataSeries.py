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

# ==[ SYSTEM IMPORTS ]====================================================
from log import LOG
try:
    import cPickle as pickle
except:
    import pickle

# ==[ USER IMPORTS ]======================================================
import systemAttributes
from network import Network

# ==[ CLASS ]=============================================================
class DataSeries:

    # ==[ CONSTANTS ]=====================================================
    DEFAULT_SCAN_TIME_IN_SECONDS = 2.5

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, name, degreesToScanPitchLowerLimit, degreesToScanPitchUpperLimit, degreesToScanYaw, pitchStepMultiplier, yawStepMultiplier):

        # --< attributes >-----
        self.name = name
        self.networks = []

        # --< control variables >-----
        self.degreesToScanPitchLowerLimit = degreesToScanPitchLowerLimit
        self.degreesToScanPitchUpperLimit = degreesToScanPitchUpperLimit
        self.degreesToScanYaw = degreesToScanYaw
        self.pitchStepMultiplier = pitchStepMultiplier
        self.yawStepMultiplier = yawStepMultiplier

        # --< calculate motor metadata >------
        self.stepsToScanPitch = int((self.degreesToScanPitchUpperLimit - self.degreesToScanPitchLowerLimit) / (systemAttributes.PITCH_MOTOR_STEP_SIZE_IN_DEGREE * self.pitchStepMultiplier))
        self.stepsToScanYaw = int(self.degreesToScanYaw / (systemAttributes.YAW_MOTOR_STEP_SIZE_IN_DEGREE * self.yawStepMultiplier))

        LOG("Data series created with parameters: \n\t"
            + "\tSteps to scan yaw: " + str(self.stepsToScanYaw) + "\n"
            + "\tSteps to scan pitch: " + str(self.stepsToScanPitch) + "\n")

    # ==[ METHODS ]=======================================================
    def printToConsole(self):

        # --< print header and name of data series >-----
        print("====================================================================")
        print("Name of dataseries: " + self.name + "\n")
        print("Number of networks found: " + str(len(self.networks)) + "\n")
        print("\nList of Networks:")

        # --< print list of networks >-----
        for tempNetwork in self.networks:
            tempNetwork.printToConsole()
            
        print("====================================================================")

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







    
