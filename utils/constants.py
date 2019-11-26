import configparser

# Initializes the configuration object and parses it
config = configparser.ConfigParser()
config.read('config.ini')

# Loading constants
PORT = config.get('API', 'PORT')