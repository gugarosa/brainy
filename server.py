import logging
from concurrent.futures import ProcessPoolExecutor

from tornado.web import Application

import utils.constants as c
from handlers.learner import LearnerHandler
from utils.process_manager import ProcessManager


class Server(Application):
    """A class to hold and bootstrap all the application services.

    """

    def __init__(self):
        """It serves as the application initialization method.

        Note that you will need to set your own arguments, handlers and
        default settings from Tornado.

        """

        # Defining the process manager
        self.process_manager = ProcessManager()

        # Creating a pool of learning workers
        self.learner_pool = ProcessPoolExecutor(max_workers=int(c.LEARNER_WORKERS))

        # Defining own arguments to be avaliable for the class
        args = {
            'config': c.config,
            'process_manager': self.process_manager
        }

        # Defining the handlers that will handle the requests
        handlers = [
            (r'/api/learner', LearnerHandler, args)
        ]

        # Overriding the Application class
        super(Server, self).__init__(handlers, debug=True, autoreload=True)

    def shutdown(self, blocking_call=True):
        """Closes the worker pools.

        Args:
            blocking_call (bool): Boolean to block itself until all pools are closed.

        """

        logging.warning("Shutting down workers pool ...")

        # Actually shutdowns the learner pool
        self.learner_pool.shutdown(blocking_call)
