# MQTT client to switch VHF and HF antenna between 6 SDR receivers

import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO
import logging
from cysystemd.journal import JournaldLogHandler

# get instance of logger object
logger = logging.getLogger('Antenna Switcher v5')
# instantiate JournaldLogHandler to hook inot systemd
journald_handler = JournaldLogHandler()
#set a formatter to include log level name
journald_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))
# add journald handler to the current logger
logger.addHandler(journald_handler)
# optionally set logging level
logger.setLevel(logging.INFO)

# setup the GPIO pins used, pin numbers refer to the R-Pi physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


outputPins = [

        True,  False, True,  False, False, False,   True,  False, False, False, False, False, # RTL-SDR
        False, False, True,  False, False, False,   True,  False, False, False, False, False, 

        True,  False, True,  True,  False, False,   False, True,  False, False, False, False, # Airspy
        False, False, False, True,  False, False,   False, True,  False, False, False, False,

        True,  False, False, False, False, False,   False, False, True,  False, False, False, # LimeSDR
        False, False, False, False, False, False,   False, False, True,  False, False, False,

        True,  False, False, False, True,  False,   False, False, False, True,  False, False, # B205
        False, False, False, False, True,  False,   False, False, False, True,  False, False, 

        True,  False, False, False, False, True,    False, False, False, False, True,  False, # Pluto 
        False, False, False, False, False, True,    False, False, False, False, True,  False,

        True,  False, False, False, True,  True,    False, False, False, False, False, True, # HackRF
        False, False, False, False, True,  True,    False, False, False, False, False, True
            ]

pinBank = 0

def on_connect(client, userdata, flags, rc ):
    logger.info ("Connected with rc: " + str(rc))
    client.subscribe("openwebrx/RX")

def on_message(client, userdata, msg):
    decoded_payload = msg.payload.decode('utf-8')
    rx_payload = json.loads(decoded_payload)

    global pinBank
    
    if "freq" in rx_payload:
        freq = rx_payload['freq']
        if freq < 60000000:
            antennaOffset = 0
            logger.info("Antenna = HF")
        else:
            antennaOffset = 12
            logger.info("Antenna = VHF")
    else:
        logger.warning("...no freq...")
        antennaOffset = 12   # set to VHF antenna be default     

    if "source" in rx_payload:
        rcvr = rx_payload['source']
        
        match rcvr:
            case "RTL-SDR":
                logger.info("Receiver: RTL-SDR")
                pinBank = 0 + antennaOffset
            case "AirspyHF+":
                logger.info("Reciever: AirspyHF+")
                pinBank = 24 + antennaOffset
            case "LimeSDR":
                logger.info("Receiver: LimeSDR")
                pinBank = 48 + antennaOffset
            case "B205mini":
                logger.info("Receiver: B205mini")
                pinBank = 72 + antennaOffset
            case "Pluto":
                logger.info("Receiver: Pluto")
                pinBank = 96 + antennaOffset
            case "HackRF":
                logger.info("Receiver: HackRF")
                pinBank = 120 + antennaOffset 
            case _:
                logger.warning("...Unknown Receiver Type...")
                pinBank = 0
    else:
        logger.warning("...no receiver source...")

# Antenna switch pins
    GPIO.output(11, outputPins[0+pinBank])
    GPIO.output(13, outputPins[1+pinBank])
    GPIO.output(15, outputPins[2+pinBank])
    GPIO.output(16, outputPins[3+pinBank])
    GPIO.output(18, outputPins[4+pinBank])
    GPIO.output(22, outputPins[5+pinBank])
#LED indicator pins
    GPIO.output(40, outputPins[6+pinBank])
    GPIO.output(38, outputPins[7+pinBank])
    GPIO.output(36, outputPins[8+pinBank])
    GPIO.output(32, outputPins[9+pinBank])
    GPIO.output(26, outputPins[10+pinBank])
    GPIO.output(24, outputPins[11+pinBank])

    logger.info("GPIO PinBank: " + str(outputPins[pinBank:pinBank+12]))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()

