# ========================================================================
# Title:        StepperMotor
# Author:       Jonas Buuck
# Date:         04.03.2021
# Description: Class for serial communication with ESP32
#
# --< LOG >-----
# 04.03.2021 -> class created by Jonas
# 04.03.2021 -> constructor implemented
# 04.03.2021 -> main outline of getDataPoint Method
# 05.03.2021 -> 
# ========================================================================

# ==[ IMPORTS ]===========================================================
# --< logging >------
from log import LOG

# --< user definded exceptions >-----
from exceptions import NoNetworksFoundException
from exceptions import RssiValueTransmissionException
from exceptions import SsidLengthException

# --< user defined classes >-----
from network import Network
from dataPoint import DataPoint

# --< library classes >-----
import serial
import time

# ==[ CLASS ]=============================================================
class DataAccessor:

    # --< STATIC SERIAL PARAMETERS >-----
    BAUDRATE = 19200
    DEFAULT_RASPBERRY_PORTNAME = "/dev/ttyS0"
    SCAN_REQUEST_BYTE = b'\x22'
    NETWORK_VALID_BYTE = b'\x11'
    SSID_NUMBER_OF_BYTES = 32
    RSSI_NUMBER_OF_BYTES = 1 
    SERIAL_TIMEOUT_IN_SECONDS = 5

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self):

        # --< open serial port >-----
        self.serialPort = serial.Serial()
        self.serialPort.baudrate = DataAccessor.BAUDRATE
        self.serialPort.port = DataAccessor.DEFAULT_RASPBERRY_PORTNAME
        self.serialPort.stopbits = serial.STOPBITS_ONE
        self.serialPort.timeout = DataAccessor.SERIAL_TIMEOUT_IN_SECONDS
        self.serialPort.open()

        LOG("Serial Port " + DataAccessor.DEFAULT_RASPBERRY_PORTNAME + " opened @" + str(DataAccessor.BAUDRATE))

    # ==[ METHODS ]=======================================================
    def getDataPoint(self, x, y):

        # --< local variables >-----
        bytesWritten = 0
        numberOfNetworksFound = 0
        tempListOfNetworks = []
        tempListOfDataPoints = []

        LOG("Requesting scan from ESP32")

        # --< request data scan >-----
        bytesWritten = self.serialPort.write(DataAccessor.SCAN_REQUEST_BYTE)
        LOG("Request transmitted with " + str(bytesWritten) + " byte")

        # --< read number of networks >-----
        numberOfNetworksFound = int.from_bytes(self.serialPort.read(), byteorder = "big", signed = True)
        if(numberOfNetworksFound <= 0):
            raise NoNetworksFoundException("No Networks found or no response from ESP32")

        LOG(str(numberOfNetworksFound) + " networks found in current scan")

        # --< write number of networks back to ESP >-----
        self.serialPort.write(numberOfNetworksFound.to_bytes(1,'big')) # convert int to byte and send via serial

        # --< read networks >-----
        LOG("\tReading networks")

        for j in range(numberOfNetworksFound):

            # --< get rssi values >-----
            rssi = int.from_bytes(self.serialPort.read(DataAccessor.RSSI_NUMBER_OF_BYTES), byteorder = "big", signed = True)
            rssiCheck = int.from_bytes(self.serialPort.read(DataAccessor.RSSI_NUMBER_OF_BYTES), byteorder = "big", signed = True)

            # --< check if rssi values match >-----
            if (rssi != rssiCheck):
                serialPort.reset_input_buffer()
                raise RssiValueTransmissionException("RSSI value mismatch in current scan")

            if((rssi == 0) or (rssiCheck == 0)):
                raise RssiValueTransmissionException("Rssi timeout") 


            LOG("\tRSSI value for network [" + str(j + 1) + "/" + str(numberOfNetworksFound) + "] successfully received:\t" + str(rssi))

            # --< receive ssid >-----
            ssidAsBytes = self.serialPort.read(DataAccessor.SSID_NUMBER_OF_BYTES)
            ssid = ssidAsBytes.decode('utf-8')
            LOG("\t" + str(len(ssidAsBytes)) + " bytes of SSID received")
            if(len(ssidAsBytes) != DataAccessor.SSID_NUMBER_OF_BYTES): 
                serialPort.reset_input_buffer()
                raise SsidLengthException("SSID length exception")
            
            LOG("\tSSID for network [" + str(j + 1) + "/" + str(numberOfNetworksFound) + "] received with " + str(len(ssidAsBytes)) + " bytes")

            # --< write validation that network has been received >-----
            self.serialPort.write(DataAccessor.NETWORK_VALID_BYTE)
            LOG("\tNetwork [" + str(j + 1) + "/" + str(numberOfNetworksFound) + "] receive validation transmitted")

            # --< create dataPoint >-----
            tempListOfDataPoints = []
            tempListOfDataPoints.append(DataPoint(x, y, rssi))
            temp = Network(ssid, tempListOfDataPoints)
            tempListOfNetworks.append(temp)
            
            # --< LOG >-----
            LOG("\t\tSSID: " + ssid + "\n\t\t\tRSSI: " + str(rssi) + " dBm")

        # --< check list of networks >-----
        Network.checkListOfNetworks(tempListOfNetworks)

        # --< return >-----
        return tempListOfNetworks
            






    

