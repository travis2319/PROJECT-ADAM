import pandas as pd
import numpy as np
import obd
import time

connection = obd.Async('/dev/ttyACM0')
df = pd.DataFrame(columns=["Start_Time", "SPEED", "Coolant Temp", "Engine Load", "Throttle_pos_b", "End_Time"])

def new_rpm(responses):
    start_timestamp = time.time()
    speed = responses.value
    print(speed)
    df.loc[len(df)] = [start_timestamp, speed, np.nan, np.nan, np.nan, np.nan]

def coolant_temp(responses):
    temp = responses.value
    print(temp)
    df.loc[len(df) - 1, "Coolant Temp"] = temp

def engine_load(responses):
    load = responses.value
    print(load)
    df.loc[len(df) - 1, "Engine Load"] = load

def throttle_pos(responses):
    end_timestamp = time.time()
    throttle = responses.value
    print(throttle)
    df.loc[len(df) - 1, "Throttle_pos_b"] = throttle
    df.loc[len(df) - 1, "End_Time"] = end_timestamp

connection.watch(obd.commands.SPEED, callback=new_rpm)
connection.watch(obd.commands.COOLANT_TEMP, callback=coolant_temp)
connection.watch(obd.commands.ENGINE_LOAD, callback=engine_load)
connection.watch(obd.commands.THROTTLE_POS_B, callback=throttle_pos)
connection.start()

time.sleep(20)
connection.stop()

print(df)
df.to_csv('async_log.csv', mode='a')