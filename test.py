from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

SERVO_PIN_1 = 12  # SG90-1
SERVO_PIN_2 = 13

MIN_DEGREE = -90       # 000 : -90degree
MAX_DEGREE = 90       # 180 : +90degree

def main():
    factory = PiGPIOFactory()
    servo_1 = AngularServo(SERVO_PIN_1, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)
    servo_2 = AngularServo(SERVO_PIN_2, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)

    try:
        for _ in range(5):
            servo_1.angle = 60
            sleep(1.0)
            servo_2.angle = 60
            sleep(1.0)
            servo_1.angle = -60
            sleep(1.0)
            servo_2.angle = -60
            sleep(1.0)
    except KeyboardInterrupt:
        print("stop")

    return

if __name__ == "__main__":
    main()
