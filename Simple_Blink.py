# Purpose: simple demo of how to blink an LED
#
# 2019 04 30 AJL Created file

# standard library
import time

# site packages
import RPi.GPIO as GPIO

# setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Pin assignments
LED_Pin = 23
hltPin = 13 # exit program

# GPIO setup
GPIO.setup(LED_Pin, GPIO.OUT)
GPIO.setup(hltPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# init
blink_period = 1 # value is in seconds

# create an infinite loop and manage the I/O
while True:
    GPIO.output(LED_Pin, GPIO.HIGH)
    time.sleep(blink_period)
    GPIO.output(LED_Pin, GPIO.LOW)
    time.sleep(blink_period)

    if GPIO.input(hltPin):
        GPIO.cleanup()  # cleanup all GPIO
        print("Shutting Down")
        exit()


