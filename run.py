import logging
import signal
import sys

from tornado import autoreload
from tornado.ioloop import IOLoop

import utils.constants as c
from server import Server

# Enables logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Gets the logging object
logger = logging.getLogger(__name__)


def handler(signal, frame):
    """Forces the interruption signal to be intercepted by the main process.

    Args:
        signal ():
        frame ():
    
    """

    logging.warning("Terminating server")

    #
    sys.exit()


if __name__ == '__main__':
    # Logging important information
    logging.info('Starting server ...')

    # Setting the responsibility of who will receive the interruption signal
    signal.signal(signal.SIGINT, handler)

    # Logs its port
    logging.info(f'Port: {c.PORT}')

    # Creates an application
    app = Server(c.config)

    #
    autoreload.add_reload_hook(lambda: app.shutdown())

    # Servers the application on desired port
    app.listen(c.PORT)

    # Starts a IOLoop instance
    IOLoop.current().start()
