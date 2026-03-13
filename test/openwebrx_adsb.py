#Simple client to subscribe to OpenWebRx topics 

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc ):
    print ("Connected with rc: " + str(rc))
    client.subscribe("openwebrx/ADSB")

def on_message(client, userdata, msg):
    #print ("\nTopic: " + msg.topic)
    decoded_payload = msg.payload.decode('utf-8')
    #print (decoded_payload)
    adsb_payload = json.loads(decoded_payload)
    
    if "flight" in adsb_payload:
        print("Flight: " + str(adsb_payload['flight']))
        if "altitude" in adsb_payload:
            print("  altitude: " + str(adsb_payload['altitude']))
        if "speed" in adsb_payload:
            print("  speed: " + str(adsb_payload['speed']))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()

