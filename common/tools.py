# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import traceback
import time
import threading
from wetest.device import *


def screensnap_thread(device, stop, times, interval):
    print "Start"
    for i in range(times):
        if stop.is_set(): return
        try:
            logger.debug("Snap")
            device.screenshot()
            stop.wait(interval)
        except:
            stack = traceback.format_exc()
            logger.warn(stack)


class time_snap(object):
    def __init__(self, interval=10, times=30):
        self.times = times
        self.interval = interval
        self.device = get_device()
        self.stop = threading.Event()
        self.snap_thread=None

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            try:
                self.snap_thread=threading.Thread(target=screensnap_thread, args=(self.device, self.stop, self.times, self.interval))
                self.snap_thread.start()
                fn(*args, **kwargs)
            except:
                stack = traceback.format_exc()
                logger.warn(stack)
            finally:
                self.stop.set()
                pass

        return wrapped


@time_snap(interval=2, times=5)
def test():
    for i in range(3):
        logger.debug("Login {0}".format(i))
        time.sleep(5)


if __name__ == '__main__':
    test()

    print "hello"
    time.sleep(10)
    print "world"
