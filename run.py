import configparser
import logging

from tornado.ioloop import IOLoop

from server import Server

# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Gets the logging object
logger = logging.getLogger(__name__)

# Initializes the configuration object and parses it
config = configparser.ConfigParser()
config.read('config.ini')

# Loading constants
PORT = config.get('API', 'PORT')

if __name__ == '__main__':
    # Logging important information
    logging.info('Starting server ...')

    # Tries to start a tornado webserver
    try:
        # Logs its port
        logging.info(f'Port: {PORT}')

        # Creates an application
        app = Server(config)

        # Servers the application on desired port
        app.listen(PORT)

        # Starts a IOLoop instance
        IOLoop.instance().start()

    except KeyboardInterrupt:
        exit()
