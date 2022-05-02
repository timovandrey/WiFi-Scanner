# ==[ Serial Example ]=====
# Author: Jonas Buuck
# Date: 27.02.2021 


# ==[ IMPORTS ]=====
import serial
import time

# ==[ SERIAL PARAMETERS ]=====
BAUDRATE = 19200
PORTNAME = "/dev/ttyS0"
SCAN_REQUEST_BYTE = b'\x00'
SSID_NUMBER_OF_BYTES = 32
RSSI_NUMBER_OF_BYTES = 1

# ==[ VARIABLES ]=====
bytesWritten = 0
numberOfNetworksFound = 0

# --< open serial port >-----
serialPort = serial.Serial()
serialPort.baudrate = BAUDRATE
serialPort.port = PORTNAME
serialPort.stopbits = serial.STOPBITS_ONE
serialPort.timeout = 3
serialPort.open()

# --< request data scan >-----
bytesWritten = serialPort.write(SCAN_REQUEST_BYTE)
print("LOG: " + "Data request sent, bytes written: " + str(bytesWritten))

# --< read number of networks >-----
numberOfNetworksFound = int.from_bytes(serialPort.read(), byteorder = "big", signed = True)

print("LOG: " + "Number of Networks found: " + str(numberOfNetworksFound))

# --< read networks >-----
for x in range(numberOfNetworksFound):
    
    rssi = int.from_bytes(serialPort.read(RSSI_NUMBER_OF_BYTES), byteorder = "big", signed = True)
    ssid = serialPort.read(SSID_NUMBER_OF_BYTES)

    print(rssi)
    print(ssid)

  

# --< close serial port >-----
print("LOG: Closing serial port")
serialPort.close()




                            