from tornado.web import Application


class Server(Application):
    """A class to hold and bootstrap all the application services.

    """

    def __init__(self, config=None):
        """It serves as the application initialization method.

        Note that you will need to set your own arguments, handlers and
        default settings from Tornado.

        Args:
            config (ConfigParser): A ConfigParser object contaning desired variables from config.ini file.

        """

        # Defining own arguments to be avaliable for the class
        args = {
            'config': config,
        }

        # Defining the handlers that will handle the requests
        handlers = [
        ]

        # Overriding the Application class
        super(Server, self).__init__(handlers, debug=True, autoreload=True)
