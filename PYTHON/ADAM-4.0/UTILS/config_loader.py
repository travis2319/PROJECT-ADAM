import configparser

def load_config(filename="config.txt"):
    config = configparser.ConfigParser()
    config.read(filename)
    return config
