# Python 3.x
# Purpose: demo of mqtt control of a light
# mosquitto_sub -h test.mosquitto.org -t /empug/# -v

import paho.mqtt.client as mqtt
import sys
import random

# change the line below to a unique identifier (we will all see!)
my_client_id = 'EMPUG'

# change mycntr to the length in time (seconds) you want to capture messages
mycntr = 20

# broker to connect to
#broker="10.13.0.22"
broker="192.168.1.91"
broker="test.mosquitto.org"
#broker="iot.eclipse.org"

# topic to publish
topic_pub='/empug/lightcontrol'
mqtt_msg=''

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
# arg1 is python arg2 is control word
if (len(sys.argv) == 2):
    mqtt_msg =  sys.argv[1]
    print ("The MQTT message is ", sys.argv[1])

if (len(sys.argv) == 1):
    print("Missing command line argument on or off")
    exit()

# MQTT setup
print("Creating client...")

# client ID with randomly generated suffix
my_client_id = my_client_id + '_' + str(random.randint(1,999))
print("Using client ID ", my_client_id)
client = mqtt.Client(client_id=my_client_id)

#client.on_connect = on_connect
client.on_message = on_message

#client.on_log=on_log

print("Connecting to broker", broker, "...")
client.connect(broker, port=1883, keepalive=60)

print("Connected!")

# send the message to the light/LED
print("Sending message ", mqtt_msg, " with topic ", topic_pub, " to broker ", broker)
client.publish(topic_pub, payload=mqtt_msg, qos=0, retain=False)

print("Message sent!")

