# ========================================================================
# Title:        System Attributes
# Author:       Jonas Buuck, Timo Vandrey
# Date:         02.03.2021
# Description:  Class to describe all collected data.
#
# --< LOG >-----
# 08.03.2021 -> class created by Jonas
# ========================================================================

# ==[ DATA COLLECTION CONSTANTS ]=========================================
DEFAULT_ESP_SCAN_TIME_IN_SECONDS = 2.5
DEFAULT_NUMBER_OF_SCAN_RETRYS = 5

# ==[ MOTOR PHYSICAL CONSTANTS ]==========================================
# --< PITCH MOTOR >-------------------------------------------------------
PITCH_MOTOR_STEP_SIZE_IN_DEGREE = (0.346/2)

PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE = -1
PITCH_MOTOR_LOWER_LIMIT_IN_STEPS = round(PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE / PITCH_MOTOR_STEP_SIZE_IN_DEGREE)

PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE = 90
PITCH_MOTOR_UPPER_LIMIT_IN_STEPS = round(PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE / PITCH_MOTOR_STEP_SIZE_IN_DEGREE)

PITCH_MOTOR_MIN_STEP_MULIPLIER = 50
PITCH_MOTOR_MAX_STEP_MULIPLIER = 50

PITCH_MOTOR_PORTS_LIST = (12, 16, 20, 21)


# --< YAW MOTOR >---------------------------------------------------------
YAW_MOTOR_STEP_SIZE_IN_DEGREE = (0.346/2) # not safe

YAW_MOTOR_LOWER_LIMIT_IN_DEGREE = -1
YAW_MOTOR_LOWER_LIMIT_IN_STEPS = round(YAW_MOTOR_LOWER_LIMIT_IN_DEGREE / YAW_MOTOR_STEP_SIZE_IN_DEGREE)

YAW_MOTOR_UPPER_LIMIT_IN_DEGREE = 360
YAW_MOTOR_UPPER_LIMIT_IN_STEPS = round(YAW_MOTOR_UPPER_LIMIT_IN_DEGREE / YAW_MOTOR_STEP_SIZE_IN_DEGREE)

YAW_MOTOR_MIN_STEP_MULIPLIER = 1
YAW_MOTOR_MAX_STEP_MULIPLIER = 4

YAW_MOTOR_PORTS_LIST = (6, 13, 19, 26)

# ==[ LIMIT SWITCHES ]====================================================
# --< LIMIT SWITCH YAW >--------------------------------------------------
LIMIT_SWITCH_YAW_PORT = 0
# --< LIMIT SWITCH PITCH >------------------------------------------------
LIMIT_SWITCH_PITCH_PORT = 7