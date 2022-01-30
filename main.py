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

network.phy_mode('MODE_11N')
sta_if = network.WLAN(network.STA_IF)
# Assign static ip to save connection time
sta_if.ifconfig(('123.123.0.123', '255.255.255.255', '123.123.0.123', '8.8.8.8'))

try:
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASS)
        t = time.ticks_ms()
        while not sta_if.isconnected():
            machine.idle()
            if time.ticks_diff(time.ticks_ms(), t) > 7000:
                sta_if.active(False)
                print("Timeout. Could not connect.")
                machine.deepsleep(600000)
except OSError:
    sta_if.active(False)
    machine.reset()

sensor_data = HTU21D(22, 21)


def print_and_send_data_in_loop(interval):
    while True:
        hum = sensor_data.humidity
        temp = sensor_data.temperature
        print('hum: ', + hum)
        print('tmp: ', + temp)
        request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,
                                 json={'field6': round(temp, 2),
                                       'field7': int(hum)},
                                 headers=HTTP_HEADERS)
        request.close()
        time.sleep(interval)


def send_data_to_thingspeak():
    hum = sensor_data.humidity
    temp = sensor_data.temperature
    request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,
                             json={'field6': round(temp, 2),
                                   'field7': int(hum)},
                             headers=HTTP_HEADERS)
    print(temp, hum)
    request.close()
    sta_if.active(False)


def go_deep_sleep(interval: int):
    # milliseconds 10000 milliseconds = 10sec
    machine.deepsleep(interval)


send_data_to_thingspeak()
go_deep_sleep(1800000)
