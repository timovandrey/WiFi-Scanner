from stepperMotor import StepperMotor
import systemAttributes
import RPi.GPIO as GPIO
import time

motor = StepperMotor("Test Motor", systemAttributes.PITCH_MOTOR_PORTS_LIST, systemAttributes.PITCH_MOTOR_LOWER_LIMIT_IN_STEPS, systemAttributes.PITCH_MOTOR_UPPER_LIMIT_IN_STEPS)
ports = (12, 16, 20, 21)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

# enable A, B
GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)

GPIO.setup(ports, GPIO.OUT)

#GPIO.output(12, 0)
#GPIO.output(16, 0)
#GPIO.output(20, 0)
#GPIO.output(21, 0)

#time.sleep(4)

#GPIO.output(12, 1)
#GPIO.output(16, 0)
#GPIO.output(20, 0)
#GPIO.output(21, 1)

#time.sleep(2)

motor.turnRight(5000)

GPIO.output(12, 0)
GPIO.output(16, 0)
GPIO.output(20, 0)
GPIO.output(21, 0)

#motor.turnRight(1)