import datetime
import logging

import utils.spacy as s


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
            logging.info('Sending task to worker in the pool ...')

            # Actually consumes the task
            self._invoke_consume(task)

            logging.info('Worker has finished the task.')

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

        # Learns a new Spacy model
        model_path = s.learn(task['language'], task['samples'], task['hyperparams'])

        # Adding the time when the task has ended
        task['callback']['end_time'] = datetime.datetime.utcnow().isoformat()

        # Checks if model has been properly trained
        if model_path is None:
            # Adding an error status to the callback
            task['callback']['status'] = 'error'

            # Notify someone that the model has not been trained (callback)
            logging.info('Sending callback ...')

            # Raises a RuntimeError warning that model could not been properly trained
            raise RuntimeError('Model could not been properly trained.')

        # Adding a success status to the callback
        task['callback']['status'] = 'success'

        # Uploads model to AWS
        logging.info('Uploading model ...')

        # Deletes model from local disk
        logging.info('Deleting model from disk ...')

        # Notify someone that the model has been trained (callback)
        logging.info('Sending callback ...')
