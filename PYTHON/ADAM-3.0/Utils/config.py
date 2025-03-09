import configparser

def read_config(config_file="config.txt"):
    """Read parameters from the config file"""
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Get parameters from the config file with default values as fallback
    obd_port = config.get('Ports', 'obd_port', fallback='/dev/pts/6')
    esp8266_port = config.get('Ports', 'esp8266_port', fallback='/dev/ttyUSB0')
    esp8266_baud = config.get('Ports', 'esp8266_baud', fallback='115200')
    sensor_file = config.get('Files', 'sensor_file', fallback='sensor_names.txt')
    
    # Add new parameters with default values as fallback
    temp_csv_path = config.get('Files', 'temp_csv_path', fallback='temp.csv')
    data_csv_path = config.get('Files', 'data_csv_path', fallback='data.csv')
    server_url = config.get('Server', 'server_url', fallback='http://127.0.0.1:3000/upload')
    
    return obd_port, esp8266_port, esp8266_baud, sensor_file, temp_csv_path, data_csv_path, server_url