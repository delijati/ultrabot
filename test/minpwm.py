import enc
import config
import motor
import threading
import time


enc_t = None
pwm_range = (50, 90)


class EncoderThread(enc.EncoderReader, threading.Thread):
    def __init__(self):
        enc.EncoderReader.__init__(self)
        threading.Thread.__init__(self)


def main():
    global enc_t
    enc_t = EncoderThread()
    enc_t.start()

    with motor.motor_setup(*config.LMP, cleanup=False) as run:
        print 'Left motor'
        for i in range(*pwm_range):
            print "test with %s pwm" % (i)
            run(i)
            if enc.ENC_POS[enc.LEFT] > 0:
                print "done LEFT pwm min is %s" % (i)
                run(0)
                break
            time.sleep(2)
    time.sleep(5)
    with motor.motor_setup(*config.RMP) as run:
        print '\nRight motor'
        for i in range(*pwm_range):
            print "test with %s pwm" % (i)
            run(i)
            if enc.ENC_POS[enc.RIGHT] > 0:
                print "done RIGHT pwm min is %s" % (i)
                run(0)
                break
            time.sleep(2)
    enc_t.stop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        enc_t.stop()
        pass
