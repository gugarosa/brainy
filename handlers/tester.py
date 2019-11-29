from handlers.base import BaseHandler


class TesterHandler(BaseHandler):
    """A TesterHandler is in charge of testing a model.

    """

    def initialize(self, **kwargs):
        """Initializes the current handler.

        """

        # Gathers the config object from keyword arguments
        self.config = kwargs.get('config')

    async def post(self):
        """It defines the POST request for this handler.

        Returns:
            It will return either 'True' or 'False' along with a 'success' or an 'error' response.

        """

        pass
