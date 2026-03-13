#Simple client to subscribe to OpenWebRx topics 

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc ):
    print ("Connected with rc: " + str(rc))
    client.subscribe("openwebrx/RX")

def on_message(client, userdata, msg):
    #print ("\nTopic: " + msg.topic)
    decoded_payload = msg.payload.decode('utf-8')
    #print (decoded_payload)
    rx_payload = json.loads(decoded_payload)
    
    if "source" in rx_payload:
        print("Receiver: " + str(rx_payload['source']))
        if "freq" in rx_payload:
            print("  center freq: " + str(rx_payload['freq']))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()

