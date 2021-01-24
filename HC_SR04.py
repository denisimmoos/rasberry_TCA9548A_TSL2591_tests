
class Distance(object):

    """docstring for HC-SR04."""

    def __init__(self, GPIO_TRIGGER, GPIO_ECHO):

        self.GPIO_TRIGGER = GPIO_TRIGGER
        self.GPIO_ECHO = GPIO_ECHO

    def distance(self):

        import RPi.GPIO as GPIO
        import time

        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        time.sleep(0.01)

        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        #time.sleep(0.00001)
        time.sleep(0.01)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        ReadTime = time.time()
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()

	    # return 9999.9 if we got stuck
            if ReadTime - StartTime > 0.2:
              return 9999.9
              break

        # save time of arrival
        ReadTime = time.time()
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()

	    # return 9999.9 if we got stuck
            if ReadTime - StopTime > 0.2:
              return 9999.9
              break

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distincm = (TimeElapsed * 34300) / 2

        GPIO.cleanup()

        return distincm
