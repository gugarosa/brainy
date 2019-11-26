import tornado
import logging

from handlers.base import BaseHandler
from processors.learner_processor import LearnerProcessor


class LearnerHandler(BaseHandler):
    """A LearnerHandler defines all possible methods for learning a model.

    """

    def initialize(self, **kwargs):
        """
        """

        #
        self.config = kwargs.get('config')

        #
        self.process_manager = kwargs.get('process_manager')

        #
        self.processor = LearnerProcessor()

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        try:
            logging.info('Enqueuing learner task ...')

            # Getting request object
            res = tornado.escape.json_decode(self.request.body)

            #
            self.process_manager.add_process({'target': self.processor, 'data': res})

        # If request object was not found, reply with an error
        except:
            # Setting status to bad request
            self.set_status(400)

            # Writing back an error message
            self.finish(dict(error='Data could not be found.'))

            return False

        self.finish(dict(sucess=res))

        return True
