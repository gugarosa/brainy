from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    """A handler class is defined by its main possible requests
    and other necessary functions.

    """

    def initialize(self, **kwargs):
        """It serves as the basic initializer of every incoming request.

        """

        # Defining the configuration object
        self.config = kwargs.get('config')

    def set_default_headers(self):
        """Sets the default response headers for an incoming request.

        """

        # Setting CORS-issue related
        self.set_header('Access-Control-Allow-Origin', '*')

        # Only authorized headers should proceed
        self.set_header('Access-Control-Allow-Headers',
                        'x-requested-with, Authorization, Content-type')

        # And only allowed methods
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, PATCH, DELETE, PUT')
