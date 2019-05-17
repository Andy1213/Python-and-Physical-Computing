# Python 3.x
# Purpose: subscribe to i3 events and display

import paho.mqtt.client as mqtt
import time
import random

# change the line below to a unique identifier (we will all see!)
my_client_id = 'EMPUG'

MsgRcvd = 0

# change mycntr to the length in time (seconds) you want to capture messages
mycntr = 120

# broker to connect to
broker="10.13.0.22"
#broker="192.168.1.91"

# topic to subscribe to
#topic_sub='#'
topic_sub= 'tele/i3/inside/lights/#'
#topic_sub = 'tele/i3/inside/lights/+/STATE'
#topic_sub= 'tele/i3/inside/commons/ground-sensor-cluster/bme280/#'
#topic_sub= 'tele/i3/inside/commons/#'
#topic_sub= 'tele/i3/inside/classroom/#'
#topic_sub= '$SYS/#'
#topic_sub= '/irrigator/#'

# ********************************************************************************************************* on_connect()
# function to run after successful connection to the broker
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic_sub)

# ********************************************************************************************************* on_message()
# function that will run when a message for a subscribed topic is received
def on_message(client, userdata, message):
    print()
    print("New MQTT Message Rcvd >>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("message topic=", message.topic)
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

# ************************************************************************************************************* on_log()
# debug logging
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# *************************************************************************************************************** main()

# MQTT setup
print("Creating client...")

# update client ID with randomly generated suffix
my_client_id = my_client_id + '_' + str(random.randint(1,999))
print("Using client ID ", my_client_id)
client = mqtt.Client(client_id=my_client_id)

#client.on_connect = on_connect
client.on_message = on_message

#client.on_log=on_log

print("Connecting to broker...")
client.connect(broker, port=1883, keepalive=60)

print("Connected!")

client.subscribe(topic_sub)

while mycntr > 0:
    time.sleep(1)
    client.loop()
    mycntr = mycntr - 1
    #print(mycntr)

print("Thats all folks!")


