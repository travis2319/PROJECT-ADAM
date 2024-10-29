import pandas as pd
import numpy as np
import matplotlib
import obd
import time
import datetime

print(f"pandas version: {pd.__version__}")
print(f"numpy version: {np.__version__}")
print(f"obd version: {obd.__version__}")
print(f"matplotlib version: {matplotlib.__version__}")

# Print current time
print(time.time())
print(f"Time: {datetime.datetime.now().ctime()}")

