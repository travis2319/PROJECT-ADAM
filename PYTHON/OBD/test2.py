import obd

connection = obd.OBD("/dev/pts/3") # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions


#this code just checks if it can connect to obd serial port
#it connects to port and send a speed command and prints the response
