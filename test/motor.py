"""
Mike Kroutikov, Josip Delic (c) 2014

Test ultrabot motors.

Run this code on the BeagleBone side.

It will run wheel motors in a simple pattern:

1. Left motor runs forward for 5 seconds, then stops
2. Left motor runs in reverse for about 5 seconds, then stops
3. Right motor runs forward for 5 secs, then stops
4. Right motor runs in reverse for 5 secs, then stops.
"""
import contextlib
import time
import config

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

@contextlib.contextmanager
def motor_setup(dir1_pin, dir2_pin, pwm_pin, cleanup=True):
    """
    Sets up context for operating a motor.
    """
    # Initialize GPIO pins
    GPIO.setup(dir1_pin, GPIO.OUT)
    GPIO.setup(dir2_pin, GPIO.OUT)

    # Initialize PWM pins: PWM.start(channel, duty, freq=2000, polarity=0)
    # we can't set frequncy if we work with two pwms
    PWM.start(pwm_pin, 0)#, frequency=100)

    def run_motor(speed):
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        if speed > 0:
            GPIO.output(dir1_pin, GPIO.LOW)
            GPIO.output(dir2_pin, GPIO.HIGH)
            PWM.set_duty_cycle(pwm_pin, abs(speed))
        elif speed < 0:
            GPIO.output(dir1_pin, GPIO.HIGH)
            GPIO.output(dir2_pin, GPIO.LOW)
            PWM.set_duty_cycle(pwm_pin, abs(speed))
        else:
            GPIO.output(dir1_pin, GPIO.LOW)
            GPIO.output(dir2_pin, GPIO.LOW)
            PWM.set_duty_cycle(pwm_pin, 0)

    yield run_motor

    if cleanup:
        GPIO.cleanup()
        PWM.cleanup()

if __name__ == '__main__':
    print '====== Testing ultrabot ======='
    print '\nLeft motor should follow commands\n'

    with motor_setup(*config.LMP) as run:

        print 'Left motor: Run forward'
        for i in range(1, 11):
            run(i*10)
            time.sleep(1)
        time.sleep(5)

        print 'Left motor: Stop'
        run(0)
        time.sleep(2)

        print 'Left motor: Reverse'
        run(-50)
        time.sleep(5)

        print 'Left motor: Stop'
        run(0)

    print '\nRight motor should follow commands\n'

    with motor_setup(*config.RMP) as run:
        print 'Right motor: Run forward'
        for i in range(1, 11):
            run(i*10)
            time.sleep(1)
        time.sleep(5)

        print 'Right motor: Stop'
        run(0)
        time.sleep(2)

        print 'Right motor: Reverse'
        run(-50)
        time.sleep(5)

        print 'Right motor: Stop'
        run(0)
