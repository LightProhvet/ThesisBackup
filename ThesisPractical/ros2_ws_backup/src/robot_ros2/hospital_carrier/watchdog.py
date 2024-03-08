import threading
import time

from .odrive_axes_of import axes_of

watchdog_threads = []

def start_watchdogs(odrv):
    global watchdog_threads
    watchdog_threads = [thr for thr in watchdog_threads if thr.is_alive()]

    def watchdog_thread(axis, lock):
        interval = 0.4 # in seconds; must be definitely shorter than the interval uploaded to ODrive
        try:
            while True:
                with lock:
                    axis.watchdog_feed()
                time.sleep(interval)
        except Exception as e:
            print('Watchdog ends with an exception of type {} ({})'.format(e.__class__.__name__, e))

    for axis in axes_of(odrv):
        thr = threading.Thread(target = watchdog_thread, args = (axis.axis, axis.lock), daemon = True)
        thr.start()
        watchdog_threads.append(thr)
