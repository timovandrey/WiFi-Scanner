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
# ========================================================================

# ==[ IMPORTS ]===========================================================
from log import LOG
from exceptions import NoNetworksFoundException
from exceptions import RssiValueTransmissionException
from exceptions import SsidLengthException
from network import Network
from dataPoint import DataPoint

import serial
import time

class DataAccessor:

    # --< SERIAL PARAMETERS >-----
    BAUDRATE = 19200
    DEFAULT_RASPBERRY_PORTNAME = "/dev/ttyS0"
    SCAN_REQUEST_BYTE = b'\x00'
    NETWORK_VALID_BYTE = b'\x11'
    SSID_NUMBER_OF_BYTES = 32
    RSSI_NUMBER_OF_BYTES = 1 
    SERIAL_TIMEOUT_IN_SECONDS = 3

    def __init__(self):

        # --< open serial port >-----
        self.serialPort = serial.Serial()
        self.serialPort.baudrate = DataAccessor.BAUDRATE
        self.serialPort.port = DataAccessor.DEFAULT_RASPBERRY_PORTNAME
        self.serialPort.stopbits = serial.STOPBITS_ONE
        self.serialPort.timeout = DataAccessor.SERIAL_TIMEOUT_IN_SECONDS
        self.serialPort.open()

        LOG("Serial Port " + DataAccessor.DEFAULT_RASPBERRY_PORTNAME + " opened @" + str(DataAccessor.BAUDRATE))

    
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
        if(numberOfNetworksFound == 0):
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
                raise RssiValueTransmissionException("RSSI value mismatch in current scan")

            LOG("\tRSSI value for network [" + str(j + 1) + "/" + str(numberOfNetworksFound) + "] successfully received")

            # --< receive ssid >-----
            ssidAsBytes = self.serialPort.read(DataAccessor.SSID_NUMBER_OF_BYTES)
            ssid = ssidAsBytes.decode('utf-8')
            LOG("\tSSID for network [" + str(j + 1) + "/" + str(numberOfNetworksFound) + "] recevied with " + str(len(ssidAsBytes)) + " bytes")
            if(len(ssidAsBytes) != DataAccessor.SSID_NUMBER_OF_BYTES): raise SsidLengthException("SSID length exception")
            
            

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
            






    

