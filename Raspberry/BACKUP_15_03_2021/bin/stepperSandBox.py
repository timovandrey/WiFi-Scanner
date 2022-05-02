from stepperMotor import StepperMotor
from limitSwitch import LimitSwitch
import systemAttributes


motor = StepperMotor("Test Yaw Motor", systemAttributes.YAW_MOTOR_PORTS_LIST, systemAttributes.YAW_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.YAW_MOTOR_UPPER_LIMIT_IN_STEPS)
limitSwitch = LimitSwitch(systemAttributes.LIMIT_SWITCH_YAW_PORT)

motor.turnRight(50)
while(limitSwitch.isPressed()):
    motor.turnRight(1)

while(limitSwitch.isPressed()):
    motor.turnLeft(1)

motor.free()
