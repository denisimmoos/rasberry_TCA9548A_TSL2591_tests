class Distance(object):

    """HC-SR04 - At the moment you can mesure a distance 
       :) and in the future not more"""

    import RPi.GPIO as GPIO
    import time

    def __init__(self, GPIO_TRIGGER, GPIO_ECHO):

        self.GPIO_TRIGGER = GPIO_TRIGGER
        self.GPIO_ECHO = GPIO_ECHO

    def distance(self):

        # GPIO Mode (BOARD / BCM)
        self.GPIO.setmode(self.GPIO.BCM)

        # set GPIO direction (IN / OUT)
        self.GPIO.setup(self.GPIO_TRIGGER, self.GPIO.OUT)
        self.GPIO.setup(self.GPIO_ECHO, self.GPIO.IN)

        self.time.sleep(0.01)

        # set Trigger to HIGH
        self.GPIO.output(self.GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        #time.sleep(0.00001)
        self.time.sleep(0.01)
        self.GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = self.time.time()
        StopTime = self.time.time()

        # save StartTime
        ReadTime = self.time.time()
        while self.GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = self.time.time()

	    # return 9999.9 if we got stuck
            if ReadTime - StartTime > 0.2:
              return 9999.9
              break

        # save time of arrival
        ReadTime = self.time.time()
        while self.GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = self.time.time()

	    # return 9999.9 if we got stuck
            if ReadTime - StopTime > 0.2:
              return 9999.9
              break

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distincm = (TimeElapsed * 34300) / 2

        self.GPIO.cleanup()

        return distincm
