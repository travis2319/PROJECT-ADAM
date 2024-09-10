import obd

# obd_connector = "/dev/pts/2"  # Replace with your OBD-II port
obd_connector = "/dev/ttyACM0"
connection = obd.OBD(obd_connector) # auto-connects to USB or RF port

cmd = obd.commands.MIDS_D # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
# print(response.value.to("mph")) # user-friendly unit conversions
