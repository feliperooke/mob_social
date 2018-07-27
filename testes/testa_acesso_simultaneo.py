# https://github.com/benediktschmitt/py-filelock

import sys
from time import sleep
from filelock import FileLock
import conf


lock = FileLock("my_lock")
with lock:
    print("This is process {}.".format(sys.argv[1]))
    sleep(10)
    print("Bye.")

print conf.dir_base
