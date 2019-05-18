# Python 3.x
# Purpose: simple demo of how to blink an LED based on the position of the sun
#
# 2019 04 30 AJL Created file

# standard library
import time

# site packages
import RPi.GPIO as GPIO
import json
import urllib.request
import requests

# loop forever or run once
loop_forever = 0

# setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Pin assignments
LED_Pin = 23
hltPin = 13 # exit program
Button_Pin = 20

# GPIO setup
GPIO.setup(LED_Pin, GPIO.OUT)
GPIO.setup(hltPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# sunset check
URLall = "http://www.l3nhart.io/cgi-bin/SunRiseSunSetJSONwDST.py"
#URLall = "https://api.sunrise-sunset.org/json?lat=42.4606&lng=-83.1346"
#URLall = "http://192.168.1.91/cgi-bin/SunRiseSunSetJSONwDST.py"

while True:

    # check if we need to halt the program
    if GPIO.input(hltPin):
        GPIO.cleanup()  # cleanup all GPIO
        print("Shutting Down")
        exit()

    # check for sunset
    try:
        urlhand = requests.get(URLall)

    except:
        print ('Error SunriseSusnet.org')

    # read the raw response
    url_raw = urlhand.text
    print(url_raw)
    json_lines = urlhand.json()

    print ('Dump of json_lines >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print (json_lines)

    # pretty print the JSON
    print('Pretty print of json_lines >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(json.dumps(json_lines, indent=4, separators=(',', ': ')))

    # parse the JSON - the file only contains one line

    # get the position of the sun (up or down)
    print ('Dump of sun_pos >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    sun_pos = json_lines['TheSunIs']
    print(sun_pos)

    # convert str to int
    isun_pos = str(sun_pos)

    # switch the light on if the sun has set
    if isun_pos:
        GPIO.output(LED_Pin, GPIO.LOW)
    else:
        GPIO.output(LED_Pin, GPIO.HIGH)

    time.sleep(60)
    
    # stop the loop or keep going
    if not loop_forever:
        exit()



