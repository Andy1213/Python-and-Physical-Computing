# Python 3.x
# Purpose: simple demo of how to blink an LED based on MQTT messages
#
# 2019 04 30 AJL Created file

# standard library

# site packages
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import random
import time

# change the line below to a unique identifier (we will all see!)
my_client_id = 'EMPUG'

# loop forever or run once
loop_forever = 1

# setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Pin assignments
LED_Pin = 23
hltPin = 13 # exit program
Button_Pin = 20
led_request = 0

# GPIO setup
GPIO.setup(LED_Pin, GPIO.OUT)
GPIO.setup(hltPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# change mycntr to the length in time (seconds) you want to capture messages
mycntr = 20

# broker to connect to
#broker="10.13.0.22"
#broker="192.168.1.91"
broker="test.mosquitto.org"

# client ID with randomly generated suffix
my_client_id = my_client_id + '_' + str(random.randint(1,999))
print("Using client ID ", my_client_id)

# topic to subscribe to
topic_sub = '/empug/lightcontrol/#'

# ********************************************************************************************************* on_connect()
# function to run after succesful connection to the broker
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic_sub)

# ********************************************************************************************************* on_message()
# function that will run when a message for a subscribed topic is received
def on_message(client, userdata, message):
    global led_request
    print()
    print("New MQTT Message Rcvd >>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("message topic=", message.topic)
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print()

    my_message = str(message.payload.decode("utf-8"))

    if my_message.find("1") > -1:
        led_request = 1
        print("LED Turned ON")
        client.publish('/empug/lightstate/', payload='on', qos=0, retain=True)
        return

    if my_message.find("0") > -1:
        led_request = 0
        print("LED Turned OFF")
        client.publish('/empug/lightstate/', payload='off', qos=0, retain=True)
        return

# ********************************************************************************************************* on_log()
# debug logging
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# ********************************************************************************************************* main()
# MQTT setup
print("Creating client...")
client = mqtt.Client(client_id=my_client_id)

#client.on_connect = on_connect
client.on_message = on_message

client.on_log=on_log

print("Connecting to broker", broker, "...")
client.connect(broker, port=1883, keepalive=60)

print("Connected!")
# client.loop_forever()
#client.loop_start() #start the loop

client.subscribe(topic_sub)

while True:

    client.loop()

    # check if we need to halt the program
    if GPIO.input(hltPin):
        GPIO.cleanup()  # cleanup all GPIO
        print("Shutting Down")
        exit()

    # switch the light on if the sun has set
    if led_request:
        GPIO.output(LED_Pin, GPIO.HIGH)
    else:
        GPIO.output(LED_Pin, GPIO.LOW)

    # stop the loop or keep going
    if not loop_forever:
        print("MQTT loop stopped")
        exit()



