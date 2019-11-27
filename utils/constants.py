import configparser

# Initializes the configuration object
config = configparser.ConfigParser()

# Parses the configuration object
config.read('config.ini')

# Loading constants
PORT = config.get('API', 'PORT')
LEARNER_WORKERS = config.get('WORKERS', 'LEARNER')
GPU_MAX_LOAD = config.get('GPU', 'MAX_LOAD')
GPU_MAX_MEMORY = config.get('GPU', 'MAX_MEMORY')