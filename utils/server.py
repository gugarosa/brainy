import logging
from concurrent.futures import ProcessPoolExecutor

from tornado.web import Application

import utils.constants as c
from handlers.predictor import PredictorHandler
from handlers.tester import TesterHandler
from handlers.trainer import TrainerHandler
from utils.process_manager import ProcessManager


class Server(Application):
    """The Server class holds and bootstraps all the application services.

    """

    def __init__(self):
        """It serves as the application initialization method.

        Note that you will need to set your own arguments, handlers and
        default settings from Tornado.

        """

        # Defining the process manager
        self.process_manager = ProcessManager()

        # Creating a pool of training workers
        self.trainer_pool = ProcessPoolExecutor(max_workers=int(c.TRAINER_WORKERS))

        # Defining own arguments to be avaliable for the class
        args = {
            'config': c.config,
            'process_manager': self.process_manager
        }

        # Defining the handlers that will handle the requests
        handlers = [
            (r'/api/trainer', TrainerHandler, args),
            (r'/api/tester', TesterHandler, args),
            (r'/api/predictor', PredictorHandler, args)
        ]

        # Overriding the Application class
        super(Server, self).__init__(handlers, debug=True, autoreload=True)

    def shutdown(self, blocking_call=True):
        """Closes the worker pools.

        Args:
            blocking_call (bool): Boolean to block itself until all pools are closed.

        """

        logging.warning("Shutting down workers pool ...")

        # Actually shutdowns the trainer pool
        self.trainer_pool.shutdown(blocking_call)
