import Adafruit_BBIO.GPIO as GPIO
import config


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
        while True:
            pass

try:
    enc = EncoderReader()
    enc.run()

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
