#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Denis Immoos (denisimmoos@gmail.com)

"""
This script reads values from 4 TSL2591 light sensors which are connected to
a TCA9548A multiplexer.

Add the following to /boot/config.txt:


dtoverlay=i2c-mux,pca9548a,addr=0x70

Install the following pip3 modules:

sudo pip3 install adafruit-circuitpython-tca9548a
sudo pip3 install adafruit-circuitpython-tsl2591

And use the following command to check if everithing is wired right:

i2cdetect -y 1

You should see the following:

     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: 70 -- -- -- -- -- -- --
    ^^ ------------ This is the multiplexer
"""

import time
import board
import busio
import adafruit_tsl2591
import adafruit_tca9548a
#from influxdb import InfluxDBClient
from os import system

# MY own Classis

from HC_SR04 import Distance

hc_sr04_0 = Distance(5, 6)
hc_sr04_1 = Distance(13, 19)
hc_sr04_2 = Distance(26, 16)
hc_sr04_3 = Distance(20, 21)
hc_sr04_4 = Distance(23, 24)

# initialize Influxdb

#influxdb = InfluxDBClient(host='localhost', port=8086)
# influxdb.drop_database('MultiLightSensors')
# influxdb.create_database('MultiLightSensors')
# influxdb.switch_database('MultiLightSensors')
# influxdb.create_retention_policy(name='MultiLightSensors', duration="48h",
#                                 replication=1, database='MultiLightSensors', default=False)

# Create I2C bus as normal
i2c = busio.I2C(board.SCL, board.SDA)

# for x in i2c.scan():
#  print(hex(x))

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# For each sensor, create it using the TCA9548A
# channel instead of the I2C object
tsl0 = adafruit_tsl2591.TSL2591(tca[0])
tsl1 = adafruit_tsl2591.TSL2591(tca[1])
tsl2 = adafruit_tsl2591.TSL2591(tca[2])
tsl3 = adafruit_tsl2591.TSL2591(tca[3])

# change this to false if you want Robbi to go into a dark corner
reverse_direction = True

# Robbies comfort zone
comfort_zone = 12.0

while True:

    #
    # distance sensors
    #
    print("-" * 80)

    dist_sensors = {
        "green": float(hc_sr04_0.distance()),
        "blue": float(hc_sr04_1.distance()),
        "yellow": float(hc_sr04_2.distance()),
        "top": float(hc_sr04_3.distance()),
        "red": float(hc_sr04_4.distance()),
    }

    print("\n")
    print("distance:")
    print("\n")
    for each in dist_sensors.keys():
        print(each + ": " + str(dist_sensors[each]))

    print("\n")

    #
    # Light sensors
    #

    sensors = {}
    sort_orders = {}

    # system('clear')

    print("-" * 80)

    for each in ['lux', 'full_spectrum', 'infrared', 'visible']:

        sensors[each] = {
            "yellow": float(getattr(tsl3, each)),
            "blue": float(getattr(tsl2, each)),
            "green": float(getattr(tsl1, each)),
            "red": float(getattr(tsl0, each)),
        }

        sort_orders[each] = sorted(sensors[each].items(
        ), key=lambda x: x[1], reverse=reverse_direction)

        sensors[each]['first'] = [sort_orders[each][0][0],
                                  sort_orders[each][0][1]]

        sensors[each]['second'] = [sort_orders[each][1][0],
                                   sort_orders[each][1][1]]

        sensors[each]['third'] = [sort_orders[each][2][0],
                                  sort_orders[each][2][1]]

        sensors[each]['fourth'] = [sort_orders[each][3][0],
                                   sort_orders[each][3][1]]

        print("\n")
        print(each + ": \n")
        print(sensors[each]['first'])
        print(sensors[each]['second'])
        print(sensors[each]['third'])
        print(sensors[each]['fourth'])

    print("\n")

#    json_body = [
#        {
#            "measurement": "MultiLightSensors",
#            "tags": {
#                "SensorId": "tsl0"
#            },
#            "fields": {
#                "lux": float(sensors['lux']['red']),
#                "full_spectrum": float(sensors['full_spectrum']['red']),
#                "visible": float(sensors['visible']['red']),
#                "infrared": float(sensors['infrared']['red']),
#            }
#        },
#        {
#            "measurement": "MultiLightSensors",
#            "tags": {
#                "SensorId": "tsl1"
#            },
#            "fields": {
#                "lux": float(sensors['lux']['green']),
#                "full_spectrum": float(sensors['full_spectrum']['green']),
#                "visible": float(sensors['visible']['green']),
#                "infrared": float(sensors['infrared']['green']),
#            }
#        },
#        {
#            "measurement": "MultiLightSensors",
#            "tags": {
#                "SensorId": "tsl2"
#            },
#            "fields": {
#                "lux": float(sensors['lux']['blue']),
#                "full_spectrum": float(sensors['full_spectrum']['blue']),
#                "visible": float(sensors['visible']['blue']),
#                "infrared": float(sensors['infrared']['blue']),
#            }
#        },
#        {
#            "measurement": "MultiLightSensors",
#            "tags": {
#                "SensorId": "tsl3"
#            },
#            "fields": {
#                "lux": float(sensors['lux']['yellow']),
#                "full_spectrum": float(sensors['full_spectrum']['yellow']),
#                "visible": float(sensors['visible']['yellow']),
#                "infrared": float(sensors['infrared']['yellow']),
#            }
#        },
#    ]

    # influxdb.write_points(json_body)

    if dist_sensors['blue'] < comfort_zone:
        system('espeak "hey, take your dirty hands of of me"')
    else:
        if sensors['full_spectrum']['first'][0] == 'blue':
            system('espeak "The brightest sensor is ' + sensors['full_spectrum']['first'][0] + '"')
            system('espeak "so I will continue"')

    if dist_sensors['red'] < comfort_zone:
        system('espeak "hey, is there a me too movement for robots. Stop it !"')
    else:
        if sensors['full_spectrum']['first'][0] == 'red':
            system('espeak "The brightest sensor is ' + sensors['full_spectrum']['first'][0] + '"')
            system('espeak "so I will  turn left"')

    if dist_sensors['yellow'] < comfort_zone:
        system('espeak "hey, do not touch my circuits. Bastard !"')
    else:
        if sensors['full_spectrum']['first'][0] == 'yellow':
            system('espeak "The brightest sensor is ' + sensors['full_spectrum']['first'][0] + '"')
            system('espeak "so I will turn right"')

    if dist_sensors['green'] < comfort_zone:
        system('espeak "mmmm, touch my booty I like it !"')
    else:
        if sensors['full_spectrum']['first'][0] == 'green':
            system('espeak "The brightest sensor is ' + sensors['full_spectrum']['first'][0] + '"')
            system('espeak "so I will roll back"')

    time.sleep(0.1)
