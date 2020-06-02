import paho.mqtt.client as paho
import numpy as np
import matplotlib.pyplot as plt
import time as t
mqttc = paho.Client("python 2")

# Settings for connection
host = "localhost"
topic= "Wutong"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

#mqttc.publish(topic, "start")
for i in range(10):
    if (i % 3 == 0):
        mqttc.publish(topic, "t")
    else:
         mqttc.publish(topic, "n")
    t.sleep(1)
mqttc.disconnect()