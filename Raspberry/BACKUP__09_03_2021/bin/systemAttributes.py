# ========================================================================
# Title:        System AttributesS
# Author:       Jonas Buuck, Timo Vandrey
# Date:         02.03.2021
# Description:  Class to describe all collected data.
#
# --< LOG >-----
# 08.03.2021 -> class created by Jonas
# ========================================================================

DEFAULT_ESP_SCAN_TIME_IN_SECONDS = 2.5

# ==[ MOTOR PHYSICAL CONSTANTS ]==========================================
# --< PITCH MOTOR >-------------------------------------------------------
PITCH_MOTOR_STEP_SIZE_IN_DEGREE = 0.346

PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE = -360
PITCH_MOTOR_LOWER_LIMIT_IN_STEPS = PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE / PITCH_MOTOR_STEP_SIZE_IN_DEGREE

PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE = 720
PITCH_MOTOR_UPPER_LIMIT_IN_STEPS = PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE / PITCH_MOTOR_STEP_SIZE_IN_DEGREE

PITCH_MOTOR_PORTS_LIST = (12, 16, 20, 21)

# --< YAW MOTOR >---------------------------------------------------------
YAW_MOTOR_STEP_SIZE_IN_DEGREE = (0.346/2)

YAW_MOTOR_LOWER_LIMIT_IN_DEGREE = -360
YAW_MOTOR_LOWER_LIMIT_IN_STEPS = PITCH_MOTOR_LOWER_LIMIT_IN_DEGREE / PITCH_MOTOR_STEP_SIZE_IN_DEGREE

YAW_MOTOR_UPPER_LIMIT_IN_DEGREE = 360
YAW_MOTOR_UPPER_LIMIT_IN_STEPS = PITCH_MOTOR_UPPER_LIMIT_IN_DEGREE / PITCH_MOTOR_STEP_SIZE_IN_DEGREE

YAW_MOTOR_PORTS_LIST = (6, 13, 19, 26)