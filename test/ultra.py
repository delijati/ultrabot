import time
import Adafruit_BBIO.GPIO as GPIO
import config
import numpy as np

# trigger duration
DECPULSETRIGGER = 0.0001
# loop iterations before timeout called
INTTIMEOUT = 2100


def setup():
    print "setup..."
    for trigger, echo in config.ULTRAS:
        GPIO.setup(echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.output(trigger, False)


def measure(trigger, echo):
    GPIO.output(trigger, True)
    time.sleep(DECPULSETRIGGER)
    GPIO.output(trigger, False)

    # Wait for echo to go high (or timeout)
    intcountdown = INTTIMEOUT

    while (GPIO.input(echo) == 0 and intcountdown > 0):
        intcountdown = intcountdown - 1

    # If echo is high
    if intcountdown > 0:

        # Start timer and init timeout countdown
        echostart = time.time()
        intcountdown = INTTIMEOUT

        # Wait for echo to go low (or timeout)
        while (GPIO.input(echo) == 1 and intcountdown > 0):
            intcountdown = intcountdown - 1

        # Stop timer
        echoend = time.time()

        # Echo duration
        echoduration = echoend - echostart
        intdistance = (echoduration*1000000) / 58.0
        return intdistance


try:
    print "running..."
    setup()
    data = [[], [], [], [], []]
    count = 10
    for i in range(count):
        i = 0
        for trigger, echo in config.ULTRAS:
            dist = measure(trigger, echo)
            data[i].append(dist)
            i += 1
    sen = ('fm', 'br', 'fl', 'fr', 'bl')
    for idx, i in enumerate(data):
        mean = np.mean(i)
        print "%s: mean %.2f cm min: %.2f cm max: %.2f cm diff: %.2f cm" % (
            sen[idx], mean, min(i), max(i), max(i) - min(i))

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
