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
from limitSwitch import LimitSwitch
import systemAttributes
from log import LOG

# ==[ CLASS DEFINITION ]==================================================
class AntennaFiniteStateMachine:

    # --< FILENAMES >-----------------------------------------------------
    YAW_MOTOR_FILE_NAME = "YAW_MOTOR_PICKLE.pickle"
    PITCH_MOTOR_FILE_NAME = "PITCH_MOTOR_PICKLE.pickle"

    # --< STATE MESSAGE >------------------------------------------------
    STATUS_MESSAGE_IDLE = "Waiting for scan request"
    STATUS_MESSAGE_COLLECTING_DATA = "Collecting data"
    STATUS_MESSAGE_MOVING_MOTORS = "Moving Motors"
    STATUS_MESSAGE_ESP_COMMUNICATION_ERROR = "No response from ESP"

    # ==[ CONSTRUCTOR ]===================================================
    def __init__(self):

        # --< interface variables >---------------------------------------
        self.IStartScan = False
        self.IScanFinished = False
        self.IRunningScan = False
        self.IQuitError = False
        self.IStatusMessage = AntennaFiniteStateMachine.STATUS_MESSAGE_IDLE
        self.IDataSeries = None

        self.ICurrentProgress = 0

        # --< create state >----------------------------------------------
        self.state = AntennaState.IDLE

        # --< create motor instances from pickle or create new >----------
        try: 
            self.yawMotor = StepperMotor.unpickle(AntennaFiniteStateMachine.YAW_MOTOR_FILE_NAME)
            self.yawMotor.openPorts()
            LOG("Yaw motor loaded from file")
        except OSError:
            self.yawMotor = StepperMotor("Yaw Motor", systemAttributes.YAW_MOTOR_PORTS_LIST, systemAttributes.YAW_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.YAW_MOTOR_UPPER_LIMIT_IN_STEPS)
            self.yawMotor.pickle(AntennaFiniteStateMachine.YAW_MOTOR_FILE_NAME)
            self.yawMotor.openPorts()
            LOG("Yaw motor not found, instance created")
        try:
            self.pitchMotor = StepperMotor.unpickle(AntennaFiniteStateMachine.PITCH_MOTOR_FILE_NAME)
            self.pitchMotor.openPorts()
            LOG("Pitch motor loaded from file") 
        except OSError:    
            self.pitchMotor = StepperMotor("Pitch Motor", systemAttributes.PITCH_MOTOR_PORTS_LIST, systemAttributes.PITCH_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.PITCH_MOTOR_UPPER_LIMIT_IN_STEPS)
            self.pitchMotor.pickle(AntennaFiniteStateMachine.PITCH_MOTOR_FILE_NAME)
            self.pitchMotor.openPorts()
            LOG("Pitch motor not found, instance created")

        # --< create limit switch instances >-----------------------------
        self.limitSwitchYaw = LimitSwitch(systemAttributes.LIMIT_SWITCH_YAW_PORT)
        self.limitSwitchPitch = LimitSwitch(systemAttributes.LIMIT_SWITCH_PITCH_PORT)
        LOG("Limit switched created")

        # --< create data accessor instance >-----
        self._dataAccessor = DataAccessor()
        LOG("Data accessor created")

        # --< create dataSeries to work with @scan >----------------------
        self._dataSeries = None

        # --< create memory variables for scan >--------------------------
        self.MCurrentArrayIndexYaw = 0
        self.MCurrentArrayIndexPitch = 0
        self.MCurrentProgress = 0

    # ==[ METHODS ]=======================================================
    def changeStateTo(self, STATE_TO_CHANGE_TO):
        self.state = STATE_TO_CHANGE_TO

        LOG("==> Changing state to: " + STATE_TO_CHANGE_TO.name)
        return

    # --< run method >----------------------------------------------------  
    # always returns if state changes
    def run(self):
        # ==[ STATE: IDLE ]===============================================
        # waiting for start command
        # if start command is given, check parameters and change state to initial setup
        if (self.state == AntennaState.IDLE):

            # --< set status message >-----
            self.IStatusMessage = AntennaFiniteStateMachine.STATUS_MESSAGE_IDLE

            # --< if start command is set >-----
            if(self.IStartScan == True):

                # log
                LOG("Starting new scan")

                # set interface variables
                self.IStartScan = False
                self.IScanFinished = False
                self.ICurrentProgress = 0
                self.IRunningScan =  True

                # copy IDataSeries to working data series
                self._dataSeries = copy.deepcopy(self.IDataSeries)

                # reset memory variables
                self.MCurrentArrayIndexYaw = 0
                self.MCurrentArrayIndexPitch = 0
                self.MCurrentProgress = 0

                # change state and return
                self.changeStateTo(AntennaState.INITIAL_SETUP)
                return
                
        # ==[ STATE: INITIAL SETUP ]======================================
        if(self.state == AntennaState.INITIAL_SETUP):

            # --< run yaw motor to initial position >---------------------
            while (self.limitSwitchYaw.isPressed()):
                self.yawMotor.turnLeft(1)
            self.yawMotor.stepCount = 0
            LOG("Yaw motor reached limit switch")

            # --< run pitch motor to initial position >-------------------
            while (self.limitSwitchPitch.isPressed()):
                self.pitchMotor.turnLeft(1)
            self.pitchMotor.stepCount = 0    
            LOG("Pitch motor reached limit switch")

            # run pitch motor to start position
            stepsToStartPosition = round((self._dataSeries.degreesToScanPitchUpperLimit - systemAttributes.PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE) / systemAttributes.PITCH_MOTOR_STEP_SIZE_IN_DEGREE)
            LOG("Making " + str(stepsToStartPosition) + " steps to start position")
            self.pitchMotor.turnLeft(stepsToStartPosition)
            
            # change to COLLECT_DATA
            self.changeStateTo(AntennaState.COLLECT_DATA)


        # ==[ STATE: COLLECT DATA ]=======================================
        if(self.state == AntennaState.COLLECT_DATA):

            self.IStatusMessage = AntennaFiniteStateMachine.STATUS_MESSAGE_COLLECTING_DATA
            
            # --< retry loop if error occurs >----------------------------
            currentScanSuccessful = False # memory variable to check is state can be changed

            for retry in range(systemAttributes.DEFAULT_NUMBER_OF_SCAN_RETRYS):

                # --< try to get data and save to _dataseries >-----------
                try:
                    self._dataAccessor.addDataPoint(self.MCurrentArrayIndexYaw, self.MCurrentArrayIndexPitch, self._dataSeries)
                    currentScanSuccessful = True
                    break
                except SsidLengthException:
                    LOG("======> SSID exception catched, retrys: " + str(retry) + " <======")
                    
                except RssiValueTransmissionException as e:
                    LOG("======> RSSI exception catched, retrys: " + str(retry) + " message" + str(e) + " <======")
                
                except NoNetworksFoundException:
                    LOG("======> Network not found exception catched, retrys: " + str(retry) + " <======")
                
            # --< for loop done, determine if state has to be changed >-----
            # if error occured
            if(currentScanSuccessful == False):
                self.IStatusMessage = AntennaFiniteStateMachine.STATUS_MESSAGE_ESP_COMMUNICATION_ERROR
                self.changeStateTo(AntennaState.ERROR)
                return

            # if end of scan reached
            if(self.MCurrentProgress == self._dataSeries.getNumberOfArrayEntrys()):
                self.changeStateTo(AntennaState.FINAL_PROCESS)
                return

            # if not end of scan
            else:
                # increment progress interface and control variable
                self.ICurrentProgress += 1 
                self.MCurrentProgress += 1
                LOG("PROGRESS: " + str(self.ICurrentProgress) + "/" + str(self._dataSeries.stepsToScanYaw * self._dataSeries.stepsToScanPitch))

                # change state
                self.changeStateTo(AntennaState.MOVE_MOTORS)
                return

        # ==[ STATE: MOVE_MOTORS ]========================================
        if(self.state == AntennaState.MOVE_MOTORS):

            self.IStatusMessage = AntennaFiniteStateMachine.STATUS_MESSAGE_MOVING_MOTORS

            # set this as true if any motor has been moved
            motorsMoved = False

            # --< if even number of yaw index or zero >-------------------
            # drive from 0 -> stepsToScanPitch @ even numbers
            if((self.MCurrentArrayIndexYaw == 0) or ((self.MCurrentArrayIndexYaw % 2) == 0)):

                # if pitch not at stepsToScanPitch
                if(self.MCurrentArrayIndexPitch < (self._dataSeries.stepsToScanPitch - 1)):
                    # drive pitch motor for step multiplier steps
                    self.pitchMotor.turnRight(self._dataSeries.pitchStepMultiplier)

                    # next pitch array index reached, increment pitch counter
                    self.MCurrentArrayIndexPitch += 1
                    motorsMoved = True

                # if pitch at end of array
                else: 
                    # move yaw motor for step multplier steps
                    self.yawMotor.turnRight(self._dataSeries.yawStepMultiplier)   

                    # next yaw array index reached, increment yaw
                    self.MCurrentArrayIndexYaw += 1 
                    motorsMoved = True

            # --< if odd number of yaw index >----------------------------
            # drive from stepsToScanPitch -> 0 @ odd numbers
            else:
                # if pitch not at 0
                if(self.MCurrentArrayIndexPitch > 0):
                    # drive pitch motor for step multiplier steps
                    self.pitchMotor.turnLeft(self._dataSeries.pitchStepMultiplier)
                    
                    # next array index reached, decrement pitch counter
                    self.MCurrentArrayIndexPitch -= 1
                    motorsMoved = True

                # if pitch at 0
                else: 
                    # move yaw motor for step multplier steps
                    self.yawMotor.turnRight(self._dataSeries.yawStepMultiplier)    

                    # next yaw array index reached, increment yaw
                    self.MCurrentArrayIndexYaw += 1
                    motorsMoved = True

            # --< if motors did not move, something went wrong >----------
            if(motorsMoved == False):
                self.changeStateTo(AntennaState.ERROR)
                return
            else: self.changeStateTo(AntennaState.COLLECT_DATA)


        # ==[ STATE: FINAL_PROCESS ]========================================
        if(self.state == AntennaState.FINAL_PROCESS):

            # set finish interface variable
            LOG("==================== SCAN FINISHED SUCCESSFULLY ====================")
            self.IScanFinished = True

            # close motors 
            self.yawMotor.free()
            self.pitchMotor.free()
            
            self.yawMotor.pickle()
            self.pitchMotor.pickle()

            self.yawMotor = None
            self.pitchMotor = None

            # back to idle
            self.changeStateTo(AntennaState.IDLE)
            return

        # ==[ STATE: ERROR ]========================================
        if(self.state == AntennaState.ERROR):
            if(self.IQuitError == True):
                self.IQuitError = False
                self.changeStateTo(AntennaState.IDLE)




class AntennaState(Enum):
    IDLE = 1
    INITIAL_SETUP = 2
    COLLECT_DATA = 3
    MOVE_MOTORS = 4
    FINAL_PROCESS = 5
    ERROR = 99






    