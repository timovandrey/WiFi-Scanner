from stepperMotor import StepperMotor
from limitSwitch import LimitSwitch
import systemAttributes


yawMotor = StepperMotor("Test Yaw Motor", systemAttributes.YAW_MOTOR_PORTS_LIST, systemAttributes.YAW_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.YAW_MOTOR_UPPER_LIMIT_IN_STEPS)
yawMotor.openPorts()
limitSwitchYaw = LimitSwitch(systemAttributes.LIMIT_SWITCH_YAW_PORT)

pitchMotor = StepperMotor("Test Pitch Motor", systemAttributes.PITCH_MOTOR_PORTS_LIST, systemAttributes.PITCH_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.PITCH_MOTOR_UPPER_LIMIT_IN_STEPS)
pitchMotor.openPorts()
limitSwitchPitch = LimitSwitch(systemAttributes.LIMIT_SWITCH_PITCH_PORT)


# yawMotor.turnRight(10)
# while(limitSwitch.isPressed()):
#     motor.turnRight(1)

# while(limitSwitch.isPressed()):
#     motor.turnLeft(1)


yawMotor.free()
pitchMotor.free()
