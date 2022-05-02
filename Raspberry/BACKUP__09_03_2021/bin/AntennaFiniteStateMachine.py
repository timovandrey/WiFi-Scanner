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
import copy

# ==[ USER IMPORT ]=======================================================
from stepperMotor import StepperMotor
from dataAccessor import DataAccessor
from dataSeries import DataSeries
import systemAttributes

# ==[ CLASS DEFINITION ]==================================================
class AntennaFiniteStateMachine:

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self):

        # --< control variables >-----------------------------------------
        self.IStartScan = False
        self.IRunningScan = False
        self.IDataSeries = None

        # --< create state >----------------------------------------------
        self.state = AntennaState.idle

        # --< create motor instances >------------------------------------
        self.yawMotor = StepperMotor("Yaw Motor", systemAttributes.YAW_MOTOR_PORTS_LIST, systemAttributes.YAW_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.YAW_MOTOR_UPPER_LIMIT_IN_STEPS)
        self.pitchMotor = StepperMotor("Pitch Motor", systemAttributes.PITCH_MOTOR_PORTS_LIST, systemAttributes.PITCH_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.PITCH_MOTOR_UPPER_LIMIT_IN_STEPS)

        # --< create data accessor instance >-----
        self.dataAccessor = DataAccessor()

        # --< create dataSeries to work with @scan >----------------------
        self._dataSeries = None

    # ==[ METHODS ]=======================================================
    def changeStateTo(self, STATE_TO_CHANGE_TO):
        self.state = STATE_TO_CHANGE_TO

        LOG(AntennaState.STATE_TO_CHANGE_TO.name)
        return
    # --< run method >----------------------------------------------------  
    # always returns if state changes
    def run():
        # ==[ STATE: IDLE ]===============================================
        # waiting for start command
        # if start command is given, check parameters and change state to initial setup
        if (self.state == AntennaState.IDLE):

            # --< if start command is set >-----
            if(self.IStartScan == True):

                # reset control variable
                self.IStartScan = False

                # set running to read
                self.IRunningScan =  True

                # copy IDataSeries to working data series
                self._dataSeries = self.IDataSeries

                # change state and return
                self.state = self.changeStateTo(AntennaState.INITIAL_SETUP)
                return
                
        # ==[ STATE: INITIAL SETUP ]======================================
        if(self.state == AntennaState.INITIAL_SETUP):

            # --< set pitch motor to start position >-----







        

     

class AntennaState(Enum):
    IDLE = 1
    INITIAL_SETUP = 2
    COLLECT_DATA = 3
    ERROR = 99






    