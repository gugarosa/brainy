import configparser

# Initializes the configuration object
config = configparser.ConfigParser()

# Parses the configuration object
config.read('config.ini')

# Loading constants
PORT = config.get('API', 'PORT')