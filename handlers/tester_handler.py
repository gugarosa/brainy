import datetime
import logging

import tornado

from handlers.base_handler import BaseHandler
from processors.tester_processor import TesterProcessor


class TesterHandler(BaseHandler):
    """A TesterHandler is in charge of testing a model.

    """

    def initialize(self, **kwargs):
        """Initializes the current handler.

        """

        # Gathers the config object from keyword arguments
        self.config = kwargs.get('config')

        # Gathers the process manager object from keyword arguments
        self.process_manager = kwargs.get('process_manager')

        # Creates the processor for this handler
        self.processor = TesterProcessor

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        # Getting request object
        req = tornado.escape.json_decode(self.request.body)

        # Gathering the model's identifier
        _id = req['id']

        # Gathering the model's type
        _type = req['type']

        # Gathering the samples
        samples = req['samples']

        # Creating the data object
        data = {
            'id': _id,
            'type': _type,
            'samples': samples,
            'callback': {
                'start_time': datetime.datetime.utcnow().isoformat()
            }
        }

        # Tries to add a new process to the pool
        try:
            logging.info('Adding tester task to the pool ...')

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
