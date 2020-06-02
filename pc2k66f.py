import serial
import time
import paho.mqtt.client as paho
import numpy as np
import matplotlib.pyplot as plt

# MQTT setting---------------------------------------------------
mqttc = paho.Client()
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
#------------------------------------------------------------
# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x415\r\n".encode())
char = s.read(3)
print("Set MY 41.")
print(char.decode())

s.write("ATDL 0x405\r\n".encode())
char = s.read(3)
print("Set DL 40.")
print(char.decode())

s.write("ATID 0x12\r\n".encode())
char = s.read(3)
print("Set PAN ID 12.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")
#----------------------------------------------------------------
times = np.zeros(10)

for i in range(10):
    # send RPC to remote
    s.write("/Send/run\r".encode())
    print(i)
    time.sleep(1)
    line = s.readline()
    times[i] = float(line)
    
    # send the data to another python program
    for j in range(times - 1):    
        line = s.readline()
        x = float(line)
        
        line = s.readline()
        y = float(line)
        
        line = s.readline()
        z = float(line)
        
        if (x * x + y * y > z * z):
            mqttc.publish(topic, "t")
        else:
            mqttc.publish(topic, "n")
s.close()
plt.plot(range(10), times)
plt.title('# Collected data plot')
plt.xlabel('Time stamp')
plt.ylabel('number')
plt.show()
