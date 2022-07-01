from flask import Flask, g, request
from flask_cors import CORS, cross_origin
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from time import sleep
import json

SERVO_PIN_1 = 12  # SG90-1
SERVO_PIN_2 = 13

MIN_DEGREE = -90       # 000 : -90degree
MAX_DEGREE = 90       # 180 : +90degree

factory = PiGPIOFactory()
servo_1 = AngularServo(SERVO_PIN_1, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)
servo_2 = AngularServo(SERVO_PIN_2, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, pin_factory=factory)

# 初期化
servo_1.min()
sleep(1.0)
servo_1.max()
sleep(1.0)
servo_1.mid()
sleep(1.0)
servo_2.min()
sleep(1.0)
servo_2.max()
sleep(1.0)
servo_2.mid()
sleep(1.0)

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/cam', methods=['POST'])
@cross_origin(supports_credentials=True)
def post_direction():
    j = json.loads(request.json["body"])
    d = j["direction"]
    try:
        d1 = j["d1"]
        d2 = j["d2"]
    except:
        pass
    if d1 is None or d2 is None:
        d1 = 0 
        d2 = 0

    print("d1: {}, d2: {}".format(d1, d2))
    if "w" in d or "ArrowDown" in d:
        servo_1.angle = d1
        servo_2.angle = d2 - 5
        d1 = d1
        d2 = d2 - 5
        sleep(0.2)
    if "s" in d or "ArrowDown" in d:
        servo_1.angle = d1
        servo_2.angle = d2 + 5
        d1 = d1
        d2 = d2 + 5
        sleep(0.2)
    if "a" in d or "ArrowLeft" in d:
        servo_1.angle = d1 + 5
        servo_2.angle = d2
        d1 = d1 + 5
        d2 = d2
        sleep(0.2)
    if "d" in d or "ArrowRight" in d:
        servo_1.angle = d1 - 5
        servo_2.angle = d2
        d1 = d1 - 5
        d2 = d2
        sleep(0.2)
    return json.dumps({"d1": d1, "d2": d2})


if __name__ == '__main__':
    app.run(host='0.0.0.0')