# from Adafruit_SHT31 import *
from time import sleep
from SHT31D import *
from firebase import firebase

import jason
#logging.basicConfig(filename='example.log',level=logging.DEBUG)

sensor = SHT31D(address = 0x44)
#sensor = SHT31(address = 0x45)

# def print_status():
#     status = sensor.read_status()
#     is_data_crc_error = sensor.is_data_crc_error()
#     is_command_error = sensor.is_command_error()
#     is_reset_detected = sensor.is_reset_detected()
#     is_tracking_temperature_alert = sensor.is_tracking_temperature_alert()
#     is_tracking_humidity_alert = sensor.is_tracking_humidity_alert()
#     is_heater_active = sensor.is_heater_active()
#     is_alert_pending = sensor.is_alert_pending()
#     print 'Status           = {:04X}'.format(status)
#     print '  Data CRC Error = {}'.format(is_data_crc_error)
#     print '  Command Error  = {}'.format(is_command_error)
#     print '  Reset Detected = {}'.format(is_reset_detected)
#     print '  Tracking Temp  = {}'.format(is_tracking_temperature_alert)
#     print '  Tracking RH    = {}'.format(is_tracking_humidity_alert)
#     print '  Heater Active  = {}'.format(is_heater_active)
#     print '  Alert Pending  = {}'.format(is_alert_pending)

# loop = 0
firebase = firebase.FirebaseApplication("https://smartghar-bac56.firebaseio.com/, None)

def firebase_update():
    degree = sensor.temperature
    humidity = sensor.humidity

    if degree is not None and humidity is not none:
        sleep(5)
        temperature = '{0:0.02f} deg C'.format(degree)
        humid =  '{0:0.2f} %'.format(humidity)
    else:
		print('Failed to get reading. Try again!')	
		sleep(10)
    
    data = {"temp": temperature, "humidity": humidity}
    firebase.post('/TempHumid', data)

print("Temperature      Humidity")
while True:
    firebase_update()
    # degrees = sensor.temperature()
    # humidity = sensor.humidity()
    # print_status()
    # print ('{0:0.3f} deg C      {1:0.2f} %'.format(degrees,humidity))
    # print ('{0:0.2f} %'.format(humidity))
    # sensor.clear_status()
    # sensor.set_heater(True)
    # print_status()
    # sensor.set_heater(False)
    # print_status()
    # loop += 1
    # sleep(4)
    # if loop == 10:
    #     loop =0
    #     sensor.heater = True
