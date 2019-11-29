import configparser

# Initializes the configuration object
config = configparser.ConfigParser()

# Parses the configuration object
config.read('config.ini')

# Gathering and defining constants
# API's port
PORT = config.get('API', 'PORT')

# Amount of trainer workers
TRAINER_WORKERS = config.get('WORKERS', 'TRAINER')

# Amount of tester workers
TESTER_WORKERS = config.get('WORKERS', 'TESTER')

# Maximum load of GPU per process
GPU_MAX_LOAD = config.get('GPU', 'MAX_LOAD')

# Maximum memory of GPU per process
GPU_MAX_MEMORY = config.get('GPU', 'MAX_MEMORY')

# Default path to save the models
DEFAULT_PATH = 'models/'