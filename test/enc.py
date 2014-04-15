import Adafruit_BBIO.GPIO as GPIO
import config

counter_l = 0
counter_r = 0

def update_encoder_l(channel):
    global counter_l
    counter_l = counter_l + 1
    print "Encoder (left) counter updated: %d" % counter_l


def update_encoder_r(channel):
    global counter_r
    counter_r = counter_r + 1
    print "Encoder (right) counter updated: %d" % counter_r


GPIO.setup(config.Ol, GPIO.IN)
GPIO.add_event_detect(config.Ol, GPIO.RISING, callback=update_encoder_l)

GPIO.setup(config.Or, GPIO.IN)
GPIO.add_event_detect(config.Or, GPIO.RISING, callback=update_encoder_r)

try:
    while True:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
