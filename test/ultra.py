import time
import Adafruit_BBIO.GPIO as GPIO
import config

# trigger duration
decpulsetrigger = 0.0001
# loop iterations before timeout called
inttimeout = 2100

def setup():
    print "setup..."
    for trigger, echo in config.ULTRAS:
        GPIO.setup(echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.output(trigger, False)


def measure(trigger, echo):
    GPIO.output(trigger, True)
    time.sleep(decpulsetrigger)
    GPIO.output(trigger, False)

    # Wait for echo to go high (or timeout)
    intcountdown = inttimeout

    while (GPIO.input(echo) == 0 and intcountdown > 0):
        intcountdown = intcountdown - 1

    # If echo is high
    if intcountdown > 0:

        # Start timer and init timeout countdown
        echostart = time.time()
        intcountdown = inttimeout

        # Wait for echo to go low (or timeout)
        while (GPIO.input(echo) == 1 and intcountdown > 0):
            intcountdown = intcountdown - 1

        # Stop timer
        echoend = time.time()

        # Echo duration
        echoduration = echoend - echostart

    # Display distance
    if intcountdown > 0:
        intdistance = (echoduration*1000000)/58
        print "Distance = " + str(intdistance) + "cm"

        # Wait at least .01s before re trig (or in this case .1s)
        time.sleep(.1)

try:
    print "running..."
    setup()
    for i in range(5):
        print "\n*************************************\n"
        for trigger, echo in config.ULTRAS:
            print "measure trigger: %s echo: %s" % (trigger, echo)
            measure(trigger, echo)
        #print chr(27) + "[2J"

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
