import paho.mqtt.client as paho
import numpy as np
import matplotlib.pyplot as plt
import time as t
mqttc = paho.Client("python1")

# Settings for connection
host = "localhost"
topic= "Wutong"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    global j
    global tilt
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    if (str(msg.payload.decode("utf-8")) == "t"):
        tilt[j] = 1
        j = j + 1
    elif(str(msg.payload.decode("utf-8")) == "n"):
        tilt[j] = 0
        j = j + 1

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

tilt = np.zeros(100)
j = 0

mqttc.loop_start()
t.sleep(15)
mqttc.loop_stop()
mqttc.disconnect()

tilt = tilt[0:j]

plt.stem(np.linspace(0, 10, j), tilt)
plt.title('The tilt result')
plt.xlabel('Time')
plt.ylabel('Tilt or not')
plt.show()