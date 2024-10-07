import obd

def obd_connection(obd_connector):
    try:
        connection = obd.OBD(obd_connector)
        return connection
    except Exception as e:
        print(f"Error connecting to OBD-II: {e}")
        return None

def async_connection(obd_connector):
    try:
        connection = obd.Async(obd_connector)
        return connection
    except Exception as e:
        print(f"Error connecting to OBD-II asynchronously: {e}")
        return None