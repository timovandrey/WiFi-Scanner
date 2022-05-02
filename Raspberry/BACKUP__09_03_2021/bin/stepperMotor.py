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
from exceptions import MotorOutOfLimitsException

class StepperMotor:

    # ==[ CONSTANTS ]=====================================================
    NUMBER_OF_STATES = 4
    DEFAULT_STEP_DELAY_TIME = 2 * 10**(-3)
    CONTROL_VOLTAGE = 4 # V
    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, name, portList, stepsLowerLimit, stepsUpperLimit):

        # --< set name >--------------------------------------------------
        self._name = name

        # --< set pin-numbering to pin numbers >--------------------------
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # --< set states >------------------------------------------------
        self._state1 = (1,0,0,1)
        self._state2 = (1,1,0,0)
        self._state3 = (0,1,1,0)
        self._state4 = (0,0,1,1)
        
        self.states = (self._state1, self._state2, self._state3, self._state4)

        self.currentState = 0 # variable for saving current state, range = 0 - 3

        # --< port setup >------------------------------------------------
        self._portList = portList
        GPIO.setup(self._portList, GPIO.OUT)

        # --< set step count >--------------------------------------------
        self.stepCount = 0
        self._stepsLowerLimit = stepsLowerLimit
        self._stepsUpperLimit = stepsUpperLimit

    # ==[ METHODS ]=======================================================

    # --< Name: writeStateToGpio >----------------------------------------------
    # write output pattern according to given stateIndex to output pins
    def writeStateToGpio(self, stateIndex):
        GPIO.output(self._portList, self.states[stateIndex])

    # --< Name: turnRight >-----------------------------------------------
    # turn motor right for passed number of steps
    # throws exception if degree limit is reached
    def turnRight(self, numberOfSteps):

        # iterate over number of steps to make
        for step in range(numberOfSteps):

            # --< check if right turn is allowed >----------------------------
            if(self.stepCount >= self._stepsUpperLimit):
                GPIO.output(self._portList, 0)
                raise MotorOutOfLimitsException(self._name + ": motor reached upper limit of steps")

            # --< check for last state, if lower: increment >-----------------
            if(self.currentState < (StepperMotor.NUMBER_OF_STATES - 1)):
                self.currentState += 1

            # --< if currentState == 3, set state 0 >-----    
            else: self.currentState = 0

            # --< write state to pins >-----
            self.writeStateToGpio(self.currentState)

            # increment stepcount
            self.stepCount += 1

            # if not last step, delay
            if(step < (numberOfSteps - 1)):
                time.sleep(StepperMotor.DEFAULT_STEP_DELAY_TIME)









        