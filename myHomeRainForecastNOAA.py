# python 3.x
# Purpose: Get rainfall or rainfall forecast and set the raintoday flag
#
# Need to set a commandline arg to MQTT broker
#  test.mosquitto.org
#
# 2016 03 02 AJL Created file
# 2016 03 04 AJL Added time of day output in file
# 2016 03 05 AJL Added rt clock from Huzzah to output file
#                Now have option for Win vs Fedora file path
# 2016 03 25 AJL Created myHomeDataScraperDB_pi.py file from copy of myHomeDataScraper.py
# 2016 04 10 AJL Merged in chagnes from myHomeDataScraperDB_PH2.py
#                OS recogniton to determine file path
# 2016 05 01 AJL Created file from myHomeDataScraperDB_pi.py
#                Updated for EdgeWeather
#                Added p3 designator to myGetPhotonData(sVarName)
# 2016 06 26 AJL Added p3_wndgust and p3_raininmo
# 2016 11 29 AJL Some p2_ vars have been moved to p1_ corrected here. SQL will still reflect p2 names
# 2016 01 24 AJL Swapped p1 and p5 processors - remapped p1 board to p5
# 2017 05 04 AJL Rewrote WU data fetch to only retrieve data one time
# 2017 05 25 AJL MQTT publish of rainfall for Irrigator app
# 2017 10 27 AJL Trap set for exception errors when convertine RainIn to a float
# 2018 06 04 AJL Created file from copy of myHomeDataScraperDB_pi.py
#                MQTT broker is passed as an arguement
#                The __main__ check is used
# 2018 06 07 AJL Cleaned up code so daily forecast is extracted as a list
# 2018 06 12 AJL Only forecast will be published - not raintoday
# 2019 03 10 AJL Changed provider from WU to NOAA due to WY licensing change
# 2019 05 14 AJL Converted to python 3.x
#
# Seems to be working. Need to remove funcs no longer used and clean code

import urllib.request, urllib.parse, urllib.error
import json
import time
import sqlite3
import platform
import paho.mqtt.client as mqtt
import sys
import string
import unicodedata
import requests

# functions for reading from cloud sources
# *********************************************************** myGetNOAAForecast()
def myGetNOAAForecast():
    # Purpose: function to retrieve data from Weather Underground Cloud
    # 2016 03 25 AJL created file
    # 2016 03 30 AJL Only 11 calls to WU are allowed per minute - added delay between calls
    # 2016 04 09 AJL Changed fetch delay to 7 seconds from 6
    #                Stripped percent sign from WU RH data
    # 2019 03 10 AJL Changed provider to NOAA after WU licensing change
    # 2019 03 19 AJL Will return 0 (no rain) on failure

    #print "Entered myGetNOAAForecast()"

    # assume no rain in forecast - fail safe
    ChanceOfRain = 0

    # get all HTML from the URL
    #print"JSON Fetching forecast from NOAA"
    URLall = "https://forecast.weather.gov/MapClick.php?lat=42.41&lon=-83.01&FcstType=json"

    try:
        urlhand = requests.get(URLall)

    except:
        print('Error NOAAforecast')
        return ChanceOfRain

    # read the raw response
    url_raw = urlhand.text
    print(url_raw)
    json_lines = urlhand.json()

    print('Dump of json_lines >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(json_lines)

    # pretty print the JSON
    print('Pretty print of json_lines >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(json.dumps(json_lines, indent=4, separators=(',', ': ')))

    # Parse out the data - the daily forecasts are in a JSON list
    wufacstlist = json_lines['data']['weather']
    print("Dump of wufacstlist >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(json.dumps(wufacstlist, indent=4, separators=(',', ': ')))

    for item in range(0,5):
        ForecastToday = wufacstlist[item].lower()
        #print 'ForecastToday', ForecastToday
        if ForecastToday.find('showers') > 1:
            ChanceOfRain = 1
        if ForecastToday.find('rain') > 1:
            ChanceOfRain = 1
        if ForecastToday.find('thunder') > 1:
            ChanceOfRain = 1

    return ChanceOfRain

# end myGetNOAAForecast()

# End of Function Definitions >>>>>>>>>>>

# *********************************************************** main()
def main():

    # arg1 is python arg2 is broker
    if (len(sys.argv) == 2):
        thing_name =  sys.argv[1]
        print("The broker argument is ", sys.argv[1])
        broker = sys.argv[1]
        RainForecast = myGetNOAAForecast()

    if (len(sys.argv) == 1):
        thing_name = 'test.mosquitto.org'
        broker = thing_name
        RainForecast = myGetNOAAForecast()

    print("Forecast returned from myGetNOAAForecast to main() is ", RainForecast)
    if RainForecast:
        print("Rain is in the forecast!  :(")

    # MQTT
    mqttc = mqtt.Client()

    # connect to the Raspberry Pi sim broker
    mqttc.connect(broker, 1883, 60, bind_address="")

    time.sleep(1.0)
    mqttc.publish("/irrigator/subscribe/rainforecast", payload=str(RainForecast), qos=0, retain=True)

    print("Thats all folks!")

if __name__ == '__main__':	
 main()




