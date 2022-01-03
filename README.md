# htu21d-thingspeak
Simple example code of using HTU21D sensor to read temperature and humidity values and also send those values to thingspeak cloud.
This project use micropython v1.17 (2021-09-02) and ttgo t7 v1.3 board powered by 18650 li ion battery.


### Wiring


| 1 | ESP32   | HTU21D |
|---|---------|--------|
| 2 | vcc 3.3 | vcc    |
| 3 | gnd     | gnd    |
| 4 | pin 22  | scl    |
| 5 | pin 21  | sda    |

### Important

* Probably you will need to solder jumper pads on htu21d sensor
* Set wlan.active(False) right before call deep sleep to avoid internal wifi error
* Set machine.idle() while waiting for wifi connection to save battery
