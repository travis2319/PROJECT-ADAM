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
    
    return obd_port, esp8266_port, esp8266_baud, sensor_file