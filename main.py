from machine import I2C, Pin
from HTU21D import HTU21D
import machine
import network 
import urequests
import time

machine.freq(80000000)

WIFI_SSID = '*'
WIFI_PASS = '*'
HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '*'

try:
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    time.sleep(0.5)
    nic.connect(WIFI_SSID, WIFI_PASS)
    while not nic.isconnected():
        machine.idle()
except OSError:
    machine.reset()

sensor_data = HTU21D(22,21)

def print_and_send_data_in_loop(interval):
    while True:
        hum = sensor_data.humidity
        temp = sensor_data.temperature
        print('hum: ', + hum)
        print('tmp: ', + temp)
        request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY , 
        json = {'field6': round(temp, 2),
                'field7': int(hum)}, 
        headers = HTTP_HEADERS )
        request.close()
        time.sleep(interval)
    
    
def send_data_to_thingspeak():
    hum = sensor_data.humidity
    temp = sensor_data.temperature
    request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY , 
    json = {'field6': round(temp, 2),
            'field7': int(hum)}, 
    headers = HTTP_HEADERS )
    print(temp, hum)
    request.close()
    nic.active(False)
    
def go_deep_sleep(interval: int):
    # milliseconds 10000 milliseconds = 10sec
    machine.deepsleep(interval)
     
send_data_to_thingspeak()
go_deep_sleep(1800000)
    
