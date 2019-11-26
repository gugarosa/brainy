import logging
import os
import datetime

class LearnerProcessor:
    """

    """

    def consume(self, task):
        """
        This method should be invoked by workers on a pool to train a model
        parallelly. Notice that this method just shelters the actual code that
        will be executed, so any internal asynchronous exception will stay
        trapped here and logged explicitly.

        :param task: The task to be consumed.
        :return: None. If anything should be returned, it should be pickable.
        """
        try:
            logging.info('Consuming task ...')
            self._invoke_consume(task)
        except BaseException as e:
            logging.error('Asynchronous exception happened.')
            logging.exception(e)

    def _invoke_consume(self, task):
        """
        Runs the actual training job. This method runs on multiple parallel
        executors, which can be either threads or (hopefully) processes.
        Anything that this method returns should be pickable (including possible
        cython sub-objects).

        Although CPU-intensive, this task will block when uploading the trained
        model to AWS and when talking back to Beowulf (notice that the blocking
        time of the first is significantly larger than the latter).

        :param task: A dict containing the description of the task to be executed
        :return: None. If anything should be returned, it should be pickable.
        """

        logging.info('Running task ...')
