import logging

from tornado.ioloop import IOLoop

from server import Server
from utils import constants as c

# Enables logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Gets the logging object
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # Logging important information
    logging.info('Starting server ...')

    # Tries to start a tornado webserver
    try:
        # Logs its port
        logging.info(f'Port: {c.PORT}')

        # Creates an application
        app = Server(c.config)

        # Servers the application on desired port
        app.listen(c.PORT)

        # Starts a IOLoop instance
        IOLoop.instance().start()

    except KeyboardInterrupt:
        exit()
