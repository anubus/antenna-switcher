# MQTT client to switch VHF and HF antenna between 6 SDR receivers

import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO

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

        True, False, True, False, False, False,   True, False, False,False,False,False, # RTL-SDR
        False, False, True, False, False, False,   True, False, False,False,False,False, 

        True, False, True, True, False, False,    False, True, False, False, False, False, # Airspy
        False, False, False, True, False, False,    False, True, False, False, False, False,

        True, False, False, False, False, False,   False, False, True, False, False, False, # LimeSDR
        False, False, False, False, False, False,   False, False, True, False, False, False,

        True, False, False, False, True, False,    False, False, False, True, False, False, # B205
        False, False, False, False, True, False,    False, False, False, True, False, False, 

        True, False, False, False, False, True,    False, False, False, False, True, False, # Pluto 
        False, False, False, False, False, True,    False, False, False, False, True, False,

        True, False, False, False, True, True,    False, False, False, False, False, True, # HackRF
        False, False, False, False, True, True,    False, False, False, False, False, True
            ]

pinBank = 0

def on_connect(client, userdata, flags, rc ):
    print ("Connected with rc: " + str(rc))
    client.subscribe("openwebrx/RX")

def on_message(client, userdata, msg):
    #print ("\nTopic: " + msg.topic)
    decoded_payload = msg.payload.decode('utf-8')
    #print (decoded_payload)
    rx_payload = json.loads(decoded_payload)
    
    if "freq" in rx_payload:
        print("\nAntenna:", end=' ')
        freq = rx_payload['freq']
        if freq < 60000000:
            antennaOffset = 0
            print("HF", end=' ')
        else:
            antennaOffset = 12
            print("VHF", end=' ')
    else:
        print("\n...no freq...", end=' ')
        antennaOffset = 12   # set to VHF antenna be default     

    if "source" in rx_payload:
        rcvr = rx_payload['source']
        print("Receiver: ", end=' ')
        
        match rcvr:
            case "RTL-SDR":
                print("RTL-SDR")
                pinBank = 0 + antennaOffset
            case "AirspyHF+":
                print("AirspyHF+")
                pinBank = 24 + antennaOffset
            case "LimeSDR":
                print("LimeSDR")
                pinBank = 48 + antennaOffset
            case "B205mini":
                print("B205mini")
                pinBank = 72 + antennaOffset
            case "Pluto":
                print("Pluto")
                pinBank = 96 + antennaOffset
            case "HackRF":
                print("HackRF")
                pinBank = 120 + antennaOffset 
            case _:
                print("...Unknown Receiver Type...")
    else:
        print("...no source...")

    print("pinBank = ", outputPins[pinBank:pinBank+12])

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

    print("\nGPIO pins set!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()

