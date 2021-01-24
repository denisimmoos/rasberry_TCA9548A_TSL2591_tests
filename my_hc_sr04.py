#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from HC_SR04 import Distance

hc_sr04_0 = Distance(5, 6)
hc_sr04_1 = Distance(13, 19)
hc_sr04_2 = Distance(26, 16)
hc_sr04_3 = Distance(20, 21)
hc_sr04_4 = Distance(23, 24)

if __name__ == '__main__':
    try:
        while True:

            #            print(testit)
            #dist = distance(GPIO_TRIGGER, GPIO_ECHO)
            #print("Measured Distance = %.1f cm" % testit.distance)
            print("\n")
            print("--------------------------------\n")
            print("\n")

            print("hc_sr04_0: ", end = '') 
            print( hc_sr04_0.distance())

            print("hc_sr04_1: ", end = '') 
            print(hc_sr04_1.distance())

            print("hc_sr04_2: ", end = '') 
            print(hc_sr04_2.distance())

            print("hc_sr04_3: ", end = '') 
            print(hc_sr04_3.distance())

            print("hc_sr04_4: ", end = '') 
            print(hc_sr04_4.distance())

            time.sleep(0.1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
