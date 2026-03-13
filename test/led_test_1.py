# flash LEDs using lookup table, I hope

import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

outputPins = [True, False, False,False,False,False,
              False, True, False, False, False, False,
              False, False, True, False, False, False,
              False, False, False, True, False, False,
              False, False, False, False, True, False,
              False, False, False, False, False, True]

pinBank = 0

while True:

    GPIO.output(40, outputPins[0+pinBank])
    GPIO.output(38, outputPins[1+pinBank])
    GPIO.output(36, outputPins[2+pinBank])
    GPIO.output(32, outputPins[3+pinBank])
    GPIO.output(26, outputPins[4+pinBank])
    GPIO.output(24, outputPins[5+pinBank])

    print("\npinBank = ", pinBank, end=": ")
    for i in range(6):
        print(outputPins[i+pinBank], end=' ')

    pinBank = pinBank + 6;
    if pinBank > 30:
        pinBank = 0

    time.sleep(1)



