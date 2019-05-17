# Python 3.x
# Purpose: demo of mqtt publish
# mosquitto_sub -h test.mosquitto.org -t "/empug/#" -v
# mosquitto_sub -h iot.eclipse.org -t "/empug/#" -v

import paho.mqtt.client as mqtt
import time
import random

# change the line below to a unique identifier (we will all see!)
my_client_id = 'EMPUG'

# change mycntr to the length in time (seconds) you want to capture messages
mycntr = 20

# broker to connect to
#broker="10.13.0.22"
#broker="192.168.1.91"
broker="test.mosquitto.org"
#broker="iot.eclipse.org"

# topic to publish
topic_sub='/empug/#'

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

# topic to publish
topic_pub='/empug/' + my_client_id +'/'


client = mqtt.Client(client_id=my_client_id)

#client.on_connect = on_connect
client.on_message = on_message

#client.on_log=on_log

print("Connecting to broker", broker, "...")
client.connect(broker, port=1883, keepalive=60)

print("Connected!")

# subscribe to interesting things
client.subscribe(topic_sub)

while mycntr > 0:
    mycntr = mycntr - 1
    client.publish(topic_pub, payload=mycntr, qos=0, retain=False)
    print('Message sent >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('topic_pub', ' > ', mycntr)
    client.loop()
    time.sleep(10)

print("Thats  all folks!")

