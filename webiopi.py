import webiopi
import pigpio

from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

SERVO_PIN_1 = 12  # SG90-1
SERVO_PIN_2 = 13

MIN_DEGREE = -90       # 000 : -90degree
MAX_DEGREE = 90       # 180 : +90degree



factory = PiGPIOFactory()
servo_1 = AngularServo(SERVO_PIN_1, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)
servo_2 = AngularServo(SERVO_PIN_2, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)

"""以下、サーボ動作"""

# SERVO1
@webiopi.macro
def GET1(val):
    servo_1.angle = 60
    sleep(1.0)
    servo_1.angle = -60


# SERVO2
@webiopi.macro
def GET2(val):
    servo_2.angle = 60
    sleep(1.0)
    servo_2.angle = -60