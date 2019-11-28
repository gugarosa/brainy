import datetime
import logging

import tornado

from handlers.base import BaseHandler
from processors.learner_processor import LearnerProcessor


class LearnerHandler(BaseHandler):
    """A LearnerHandler defines all possible methods for learning a model.

    """

    def initialize(self, **kwargs):
        """Initializes the current handler.

        """

        # Gathers the config object from keyword arguments
        self.config = kwargs.get('config')

        # Gathers the process manager object from keyword arguments
        self.process_manager = kwargs.get('process_manager')

        # Creates the processor for this handler
        self.processor = LearnerProcessor

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        # Getting request object
        req = tornado.escape.json_decode(self.request.body)

        # Gathering the model's language
        language = req['language']

        # Gathering the samples
        samples = req['samples']

        # Gathering the hyperparams
        hyperparams = req['hyperparams']

        # Creating the data object
        data = {
            'language': language,
            'samples': samples,
            'hyperparams': hyperparams,
            'callback': {
                'start_time': datetime.datetime.utcnow().isoformat()
            }
        }

        # Tries to add a new process to the pool
        try:
            logging.info('Adding learner task to the pool ...')

            # Adding process to the pool
            self.process_manager.add_process(
                {'target': self.processor, 'data': data})

        # If process could not be added to the pool, reply with an error
        except Exception as e:
            logging.exception(e)

            # Setting status to error
            self.set_status(500)

            # Writing back an error message
            self.finish(dict(error='Failed to add a new task to the pool.'))

            return False

        # Writing back a success message
        self.finish(dict(sucess='A new task has been added to the pool.'))

        return True
