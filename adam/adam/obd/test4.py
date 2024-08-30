import pandas as pd
import numpy as np
import matplotlib
import obd
import time
import datetime
import requests
import serial

obd_connector="/dev/ttyACM0"
print(obd_connector)

obd.logger.setLevel(obd.logging.DEBUG)
connection = obd.Async(obd_connector)

# a callback that prints every new value to the console
def new_rpm(r):
    print (r.value)

connection.watch(obd.commands.COOLANT_TEMP, callback=new_rpm)
connection.start()

# the callback will now be fired upon receipt of new values

time.sleep(10)
connection.stop()
