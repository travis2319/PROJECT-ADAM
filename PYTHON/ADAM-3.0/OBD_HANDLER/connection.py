import obd # type: ignore

def Async_connection(portstr):
    try:
        connection = obd.Async(portstr)
        print(f"Connected to the OBD-II adapter on port {portstr}.")
        return connection
    except obd.OBDStatusError as e:
        print(f"Failed to connect to the OBD-II adapter on port {portstr}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def Async_close_connection(conn):
    try:
        conn.close()
        print("Connection closed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    