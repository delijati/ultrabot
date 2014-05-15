import time
import bbio
import numpy as np


ULTRAS = ((bbio.GPIO1_12, bbio.GPIO1_13),
          (bbio.GPIO0_3, bbio.GPIO0_2),
          (bbio.GPIO1_17, bbio.GPIO0_15),
          (bbio.GPIO3_21, bbio.GPIO0_14),
          (bbio.GPIO3_19, bbio.GPIO3_16),)

# trigger duration
DECPULSETRIGGER = 0.0001
# loop iterations before timeout called
INTTIMEOUT = 2100


def setup():
    print "setup..."
    for trigger, echo in ULTRAS:
        bbio.pinMode(echo, bbio.INPUT)
        bbio.pinMode(trigger, bbio.OUTPUT)
        bbio.digitalWrite(trigger, bbio.LOW)


def measure(trigger, echo):
    bbio.digitalWrite(trigger, bbio.HIGH)
    time.sleep(DECPULSETRIGGER)
    bbio.digitalWrite(trigger, bbio.LOW)

    # Wait for echo to go high (or timeout)
    intcountdown = INTTIMEOUT

    while (bbio.digitalRead(echo) == 0 and intcountdown > 0):
        intcountdown = intcountdown - 1

    # If echo is high
    if intcountdown > 0:

        # Start timer and init timeout countdown
        echostart = time.time()
        intcountdown = INTTIMEOUT

        # Wait for echo to go low (or timeout)
        while (bbio.digitalRead(echo) == 1 and intcountdown > 0):
            intcountdown = intcountdown - 1

        # Stop timer
        echoend = time.time()

        # Echo duration
        echoduration = echoend - echostart
        intdistance = (echoduration*1000000) / 58.0
        return intdistance


def loop():
    print "running..."
    data = [[], [], [], [], []]
    count = 10
    for i in range(count):
        i = 0
        for trigger, echo in ULTRAS:
            dist = measure(trigger, echo)
            data[i].append(dist)
            i += 1
    sen = ('fm', 'br', 'fl', 'fr', 'bl')
    for idx, i in enumerate(data):
        mean = np.mean(i)
        print "%s: mean %.2f cm min: %.2f cm max: %.2f cm diff: %.2f cm" % (
            sen[idx], mean, min(i), max(i), max(i) - min(i))
    bbio.stop()

bbio.run(setup, loop)
