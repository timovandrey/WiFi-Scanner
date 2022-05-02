# ========================================================================
# Title:        StepperMotor
# Author:       Jonas Buuck
# Date:         01.03.2021
# Description:  Class for operating the stepper motor safely.
#
# --< LOG >-----
# 01.03.2021 -> class created by Jonas
# ========================================================================

# ==[ IMPORTS ]===========================================================
import RPi.GPIO as GPIO
import time

class StepperMotor:
    # ==[ CONSTANTS ]=====================================================
    NUMBER_OF_STATES = 4
    DEFAULT_STEP_DELAY_TIME = 1 * 10**(-3)

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, portList, minDegree, maxDegree):

        # --< set pin-numbering to pin numbers >--------------------------
        GPIO.setmode(GPIO.BOARD)

        # --< set states >------------------------------------------------
        self.state1 = (1,0,0,1)
        self.state2 = (1,1,0,0)
        self.state3 = (0,1,1,0)
        self.state4 = (0,0,1,1)
        

        self.states = (state1, state2, state3, state4)
        self.currentState = 0

        # --< assign constructor values >---------------------------------
        self.portList = portList

        # --< set ports as outputs >--------------------------------------
        GPIO.setup(portList, GPIO.OUT)

        # --< set degree >------------------------------------------------
        self.currentDegree = 0
        self.minDegree = minDegree
        self.maxDegree = maxDegree

    # ==[ METHODS ]=======================================================

    # --< Name: writeState >----------------------------------------------
    # write output pattern according to given stateIndex to output pins
    def writeState(self, stateIndex):
        GPIO.output(self.portList, self.states[stateIndex])

    # --< Name: turnRight >-----------------------------------------------
    # turn motor one step right
    # throws exception if degree limit is reached
    def turnRight():
        # --< check if right turn is allowed >----------------------------
        if (self.currentDegree >= self.maxDegree):
            raise Exception("Degree greater than allowed")

        # --< check for last state, if lower: increment >-----------------
        if (self.currentState < (StepperMotor.NUMBER_OF_STATES - 1)):
            self.currentState += 1
        # --< if currentState == 3, set state 0 >-----    
        else self.currentState = 0
            
        # --< write state to pins >-----
        self.writeState(currentState)

    # --< Name: turnLeft >-----
    # turn motor one step left
    # throws exception if degree limit is reached
    def turnLeft():
        # --< check if right turn is allowed >-----
        if (self.currentDegree <= self.minDegree):
            raise Exception("Degree lower than allowed")

        # --< check for state 0, if higher: decrement >----
        if (self.currentState > 0):
            self.currentState -= 1
        # --< if currentState == 3, set state 0 >-----    
        else self.currentState = (StepperMotor.NUMBER_OF_STATES - 1)
            
        # --< write state to pins >-----
        self.writeState(currentState)






        