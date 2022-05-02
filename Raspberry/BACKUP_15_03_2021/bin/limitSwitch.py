# ========================================================================
# Title:        StepperMotor
# Author:       Jonas Buuck
# Date:         01.03.2021
# Description:  Class for operating the stepper motor safely.
#
# --< LOG >-----
# 01.03.2021 -> class created by Jonas
# ========================================================================

# ==[ SYSTEM IMPORTS ]====================================================
import RPi.GPIO as GPIO
import time

# ==[ USER IMPORTS ]======================================================

class LimitSwitch:

    def __init__(self, port):

        self._port = port

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._port, GPIO.IN)

    def isPressed(self):
        return GPIO.input(self._port)
