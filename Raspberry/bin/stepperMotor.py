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
try:
    import cPickle as pickle
except:
    import pickle

# ==[ USER IMPORTS ]======================================================
from exceptions import MotorOutOfLimitsException
from log import LOG

class StepperMotor:

    # ==[ CONSTANTS ]=====================================================
    NUMBER_OF_STATES = 4
    DEFAULT_STEP_DELAY_TIME = 5 * 10**(-3)
    CONTROL_VOLTAGE = 4 # V

    # pitch: right is down 
    # yaw: right is "up"

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, name, portList, stepsLowerLimit, stepsUpperLimit):

        # --< set name >--------------------------------------------------
        self._name = name

        # --< set states >------------------------------------------------
        self._state1 = (1,0,0,1)
        self._state2 = (1,1,0,0)
        self._state3 = (0,1,1,0)
        self._state4 = (0,0,1,1)
        
        self.states = (self._state1, self._state2, self._state3, self._state4)

        self.currentState = 0 # variable for saving current state, range = 0 - 3

        # --< assign list of ports >--------------------------------------
        self._portList = portList

        # --< set step count >--------------------------------------------
        self.stepCount = 0
        self._stepsLowerLimit = stepsLowerLimit
        self._stepsUpperLimit = stepsUpperLimit

    # ==[ METHODS ]=======================================================

    # --< Name: writeStateToGpio >----------------------------------------------
    # write output pattern according to given stateIndex to output pins
    def writeStateToGpio(self, stateIndex):
        GPIO.output(self._portList, self.states[stateIndex])

    # --< Name: openPorts >-----------------------------------------------
    # open GPIO ports of stepper motor
    def openPorts(self):

        # --< create ports as output ports >------
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._portList, GPIO.OUT)


    # --< Name: turnRight >-----------------------------------------------
    # turn motor right for passed number of steps
    # throws exception if degree limit is reached
    def turnRight(self, numberOfSteps):

        # iterate over number of steps to make
        for step in range(numberOfSteps):

            # --< check if right turn is allowed >----------------------------
            if(self.stepCount >= self._stepsUpperLimit):
                # stop motor
                GPIO.output(self._portList, 0)
                LOG("Exception @ " + str(self.stepCount))
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

            #  delay
            time.sleep(StepperMotor.DEFAULT_STEP_DELAY_TIME)

    # --< Name: turnLeft >-----------------------------------------------
    # turn motor right for passed number of steps
    # throws exception if degree limit is reached
    def turnLeft(self, numberOfSteps):

        # iterate over number of steps to make
        for step in range(numberOfSteps):

            # --< check if right turn is allowed >----------------------------
            if(self.stepCount <= self._stepsLowerLimit):
                # stop motor
                GPIO.output(self._portList, 0)
                LOG("Exception @ " + str(self.stepCount))
                raise MotorOutOfLimitsException(self._name + ": motor reached lower limit of steps")

            # --< check for first state, if higher: decrement >-----------------
            if(self.currentState > 0):
                self.currentState -= 1

            # --< if currentState == 0, set state 3 >-----    
            else: self.currentState = 3

            # --< write state to pins >-----
            self.writeStateToGpio(self.currentState)

            # decrement stepcount
            self.stepCount -= 1

            #  delay
            time.sleep(StepperMotor.DEFAULT_STEP_DELAY_TIME)

    def free(self):
        GPIO.output(self._portList, GPIO.LOW)

    # --< Pickles this object to a file >-----
    def pickle(self, filename):

        outfile = open(filename, 'wb')
        pickle.dump(self, outfile)
        outfile.close()
        

    # ==[ STATIC METHODS ]================================================
    # --< unpickles a file to a StepperMotor object >-----
    @staticmethod
    def unpickle(filename):
        infile = open(filename, 'rb')

        UnpickledMotor = pickle.load(infile)
        
        infile.close()

        return UnpickledMotor










        