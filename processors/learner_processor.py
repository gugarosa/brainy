import logging


class LearnerProcessor:
    """A LearnerProcessor class is in charge of consuming the learning task.

    """

    def consume(self, task):
        """This method should be invoked by the workers on a pool to actually train
        models parallelly.

        Notice that this method just shelters the actual code that will be executed,
        so any internal asynchronous exception will stay trapped here and logged explicitly.

        Args:
            task (dict): The task to be consumed.

        """

        # Tries to consume the task
        try:
            logging.info('Starting to learn model ...')

            # Actually consumes the task
            self._invoke_consume(task)

            logging.info('Finished learning model.')

        # If an exception has happened, logs it
        except Exception as e:
            logging.error('An exception has happened.')

            logging.exception(e)

    def _invoke_consume(self, task):
        """Runs the actual learning job.

        This method runs on multiple parallel executors, which can be either threads or processes.
        Anything that this method returns should be pickable (including possible
        cython sub-objects).

        Args:
            task (dict): The task to be consumed.

        """

        pass
