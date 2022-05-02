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
    # --< addDataPoint: pass current steps and dataSeries to get data points and networks @x, y >------
    def addDataPoint(self, x, y, dataSeries):

        # --< local variables >-------------------------------------------
        bytesWritten = 0            # temp container for number of bytes written to serial
        numberOfNetworksFound = 0   # number of networks found @x, y
        rssi = 0                    # container for received rssi value via serial
        rssiCheck = 0               # container for received rssi value confirmation via serial    
        ssidAsBytes = b''           # ssid as bytes, as received via serial
        ssid = ""                   # ssid as string, created from ssidAsBytes
        
        LOG("Requesting scan from ESP32")

        # --< request data scan from ESP >--------------------------------
        bytesWritten = self.serialPort.write(DataAccessor.SCAN_REQUEST_BYTE)
        LOG("Scan request transmitted with " + str(bytesWritten) + " byte")

        # --< read number of networks >-----------------------------------
        numberOfNetworksFound = int.from_bytes(self.serialPort.read(), byteorder = "big", signed = True)
        # if number of networks = 0 or no response from ESP32
        if(numberOfNetworksFound <= 0):
            raise NoNetworksFoundException("No Networks found or no response from ESP32")

        LOG(str(numberOfNetworksFound) + " networks found in current scan")

        # --< write number of networks back to ESP >----------------------
        self.serialPort.write(numberOfNetworksFound.to_bytes(1,'big')) # convert int to byte and send via serial

        # --< read networks >---------------------------------------------
        LOG("Reading networks from ESP")
    
        # --< iterate over number of networks found @x, y >---------------
        for j in range(numberOfNetworksFound):

            # --< get rssi values >---------------------------------------
            rssi = int.from_bytes(self.serialPort.read(DataAccessor.RSSI_NUMBER_OF_BYTES), byteorder = "big", signed = True)
            rssiCheck = int.from_bytes(self.serialPort.read(DataAccessor.RSSI_NUMBER_OF_BYTES), byteorder = "big", signed = True)

            # check if rssi values match
            if (rssi != rssiCheck):
                self.serialPort.reset_input_buffer()
                raise RssiValueTransmissionException("RSSI value mismatch in current scan")

            # check if timeout occured 
            if((rssi == 0) or (rssiCheck == 0)):
                self.serialPort.reset_input_buffer()
                raise RssiValueTransmissionException("Rssi timeout") 

            # --< receive ssid >------------------------------------------
            ssidAsBytes = self.serialPort.read(DataAccessor.SSID_NUMBER_OF_BYTES)
            ssid = ssidAsBytes.decode('utf-8')

            # check is ssid is valid
            if(len(ssidAsBytes) != DataAccessor.SSID_NUMBER_OF_BYTES): 
                self.serialPort.reset_input_buffer()
                raise SsidLengthException("SSID length exception")

            # --< write validation that network has been received >-----
            self.serialPort.write(DataAccessor.NETWORK_VALID_BYTE)

            # --< log successful received network >-----------------------
            LOG("Network [" + str(j + 1) + "/" + str(numberOfNetworksFound) + "] \""
                + ssid + "\" @[" + str(x) + "][" + str(y) + "]"
                + " received with " + str(rssi) + " dBm")

            # --< evaluate network, append to dataSeries list of networks >------
            networkAlreadyContained = False # flag to raise if network is already contained

            # iterate over existing networks
            for existingNetwork in dataSeries.networks:

                # if network exists already
                if(ssid == existingNetwork.ssid):
                    networkAlreadyContained = True

                    # check if rssi value is still empty
                    if(existingNetwork.dataPoints[x][y] == 0):
                        existingNetwork.dataPoints[x][y] = rssi
                        break

                    # check if rssi has already been set @x, y -> override value if new one is higher
                    if(existingNetwork.dataPoints[x][y] < rssi):
                        existingNetwork.dataPoints[x][y] = rssi
                        break

                    # received rssi value is lower than the one contained already
                    # ignore received rssi
                    LOG("\tThe current network is already contained with higher rssi value")
                    break
            
            # if network is not already contained
            if(networkAlreadyContained == False):
                LOG("This network is not contained")
                newNetwork = Network(ssid, dataSeries.stepsToScanYaw, dataSeries.stepsToScanPitch)
                newNetwork.dataPoints[x][y] = rssi
                dataSeries.networks.append(newNetwork)

        
            






    

