from time import sleep
from SHT31D import *
from firebase import firebase

import jason
import time
import datetime
#logging.basicConfig(filename='example.log',level=logging.DEBUG)

sensor = SHT31D(address = 0x44)

firebase = firebase.FirebaseApplication("https://smartghar-bac56.firebaseio.com/", None)

def firebase_update(degree, humidity):
    thisTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if degree is not None and humidity is not None:
        temperature = '{0:0.2f} deg C'.format(degree)
        humid =  '{0:0.2f} %'.format(humidity)
    else:
        print('Failed to get reading. Try again!')	
        sleep(10)
    
    # Update the average of 1 minute data to firebase
    data = { "Humid": humidity,"Temp": temperature, ,"Time":thisTime }
    firebase.post('/Room1/SHT31D', data)

def average_temphumid():
    degree = sensor.temperature()
    humidity = sensor.humidity()

    # Get the average temperature and humidity in a minute
    total_temp, total_humid = 0, 0
    for i in range(60):
        total_temp += degree
        total_humid += humidity
        sleep(1)
    
    average_temp = total_temp / 60
    average_humid = total_humid / 60

    firebase_update(average_temp, average_humid)

while True:

    average_temphumid()
    # print_status()
    # print ('{0:0.3f} deg C      {1:0.2f} %'.format(degrees,humidity))
    # print ('{0:0.2f} %'.format(humidity))
    # loop += 1
    # sleep(4)
    # if loop == 10:
    #     loop =0
    #     sensor.heater = True
