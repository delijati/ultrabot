import Adafruit_BBIO.GPIO as GPIO
import config
import time
import math

wheel_radius = 1.2  # cm
time_interval = 1.0  # seconds
ticks = 20  # holes in disc
const = (2 * math.pi * wheel_radius)/ticks


class EncoderReader(object):
    counter_l = 0
    counter_r = 0

    def __init__(self):
        GPIO.setup(config.Ol, GPIO.IN)
        GPIO.setup(config.Or, GPIO.IN)

    def update_encoder_l(self, channel):
        self.counter_l = self.counter_l + 1
        print "Encoder (left) counter updated: %d" % self.counter_l

    def update_encoder_r(self, channel):
        self.counter_r = self.counter_r + 1
        print "Encoder (right) counter updated: %d" % self.counter_r

    def run(self):
        GPIO.add_event_detect(config.Or, GPIO.RISING,
                              callback=self.update_encoder_r)
        GPIO.add_event_detect(config.Ol, GPIO.RISING,
                              callback=self.update_encoder_l)
        current_time_l = time.time()
        current_time_r = time.time()
        while True:
            if (time.time() >= current_time_l + time_interval):
                velocity_l = (
                    self.counter_l * (wheel_radius * const)
                ) / time_interval
                self.counter_l = 0
                current_time_l = time.time()
                print "velocity_l %s cm/s" % velocity_l
            if (time.time() >= current_time_r + time_interval):
                velocity_r = (
                    self.counter_r * (wheel_radius * const)
                ) / time_interval
                self.counter_r = 0
                current_time_r = time.time()
                print "velocity_r %s cm/s" % velocity_r

try:
    enc = EncoderReader()
    enc.run()

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
