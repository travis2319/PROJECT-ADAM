import pandas as pd
import numpy as np
import matplotlib
import obd
import time
import datetime
import requests
import serial

# obd_connector="/dev/ttyACM0"
obd_connector = '/dev/pts/2'
connection = obd.Async(obd_connector)

# a callback that prints every new value to the console
def new_rpm(r):
    print(r.value)

connection.watch(obd.commands.PIDS_9A, callback=new_rpm)
connection.start()

# the callback will now be fired upon receipt of new values

time.sleep(10)
connection.stop()
