import logging

import tornado

from handlers.base import BaseHandler
from processors.learner_processor import LearnerProcessor


class LearnerHandler(BaseHandler):
    """A LearnerHandler defines all possible methods for learning a model.

    """

    def initialize(self, **kwargs):
        """
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
        res = tornado.escape.json_decode(self.request.body)

        # Tries to add a new process to the pool
        try:
            logging.info('Adding learner task to the pool ...')

            # Adding process to the pool
            self.process_manager.add_process(
                {'target': self.processor, 'data': res})

        # If process could not be added to the pool, reply with an error
        except Exception as e:
            logging.exception(e)

            # Setting status to error
            self.set_status(500)

            # Writing back an error message
            self.finish(dict(error='Failed to add task to the pool.'))

            return False

        self.finish(dict(sucess='A new task has been added to the pool.'))

        return True
