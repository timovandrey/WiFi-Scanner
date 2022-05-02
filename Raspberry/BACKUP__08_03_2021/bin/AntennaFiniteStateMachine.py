# ========================================================================
# Title:        AntennaFininteStateMachine
# Author:       Jonas Buuck, Timo Vandrey
# Date:         07.03.2021
# Description:  An FSM to control the current antenna state
#
# --< LOG >-----
# 07.03.2021 -> class created by Timo
# ========================================================================

# ==[ SYSTEM IMPORT ]=====================================================
from enum import Enum

# ==[ USER IMPORT ]=======================================================
from stepperMotor import StepperMotor
from dataAccessor import DataAccessor
from dataSeries import DataSeries

# ==[ CLASS DEFINITION ]==================================================
class AntennaFiniteStateMachine:

    # ==[ CONSTANTS ]=====================================================
    MOTOR_X_STEP_SIZE_IN_DEGREE = 0.36
    MOTOR_Y_STEP_SIZE_IN_DEGREE = 0.36

    # --< motor x parameters >-----
    MOTOR_X_PORTS_LIST = (16, 18, 22, 24, 7)
    MOTOR_X_MIN_POSITION = -180
    MOTOR_X_MAX_POSITION = 180

    # --< motor y parameters >-----
    MOTOR_Y_PORTS_LIST = (1, 12, 16, 20, 21)
    MOTOR_Y_MIN_POSITION = -180
    MOTOR_Y_MAX_POSITION = 180

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self, dataSeries):

        # --< control variables >-----
        self.IDegreesToScanVerticalUpperLimit = 0
        self.IDegreesToScanVerticalLowerLimit = 0
        self.IDegreesToScanHorizontal = 0
        self.IStepSizeX = 0
        self.IStepSizeY = 0

        self.IStartScan = False

        # --< parameters extracted from control parameters @startup
        self._stepsToMakeX = 0
        self._stepsToMakeY = 0
        # --< create state >-----
        self.state = AntennaState.idle

        # --< create motor instances >-----
        self.motorX = StepperMotor(AntennaFiniteStateMachine.MOTOR_X_PORTS_LIST, AntennaFiniteStateMachine.MOTOR_X_MIN_POSITION, AntennaFiniteStateMachine.MOTOR_X_MAX_POSITION)
        self.motorY = StepperMotor(AntennaFiniteStateMachine.MOTOR_Y_PORTS_LIST, AntennaFiniteStateMachine.MOTOR_Y_MIN_POSITION, AntennaFiniteStateMachine.MOTOR_Y_MAX_POSITION)

        # --< create data accessor instance >-----
        self.dataAccessor = DataAccessor()

        # --< pass given dataSeries >-----
        self.dataSeries = dataSeries() 

    # ==[ RUN METHOD ]====================================================   
    # always returns if state changes

    def run():

        # ==[ STATE: IDLE ]===============================================
        # waiting for start command
        # if start command is given, check parameters and change state to initial setup
        if (self.state == AntennaState.idle):
            # --< if start command is set >-----
            if(self.IStartScan == True):
                self.IStartScan = False

                # --< check parameters >-----
                if(self.IDegreesToScanVerticalLowerLimit >= self.IDegreesToScanVerticalUpperLimit):
                    self.state = AntennaState.error
                    return

                # --< is everything ready to start process >-----

                # --< calcualte steps to go >-----
                self._stepsToMakeY = int(((self.IDegreesToScanVerticalUpperLimit - self.IDegreesToScanVerticalLowerLimit) / AntennaFiniteStateMachine.MOTOR_Y_STEP_SIZE_IN_DEGREE))
                self._stepsToMakeX = int(((self.IDegreesToScanHorizontal) / AntennaFiniteStateMachine.MOTOR_X_STEP_SIZE_IN_DEGREE))
                self.state = AntennaState.initialSetup
                return
                
        # ==[ STATE: INITIAL SETUP ]======================================
        if(self.state == AntennaState.initialSetup):




        

     

class AntennaState(Enum):
    idle = 1
    initialSetup = 2
    collectData = 3
    error = 99






    