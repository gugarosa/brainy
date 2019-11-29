import datetime
import logging
import os

import utils.constants as c
import utils.file as f
from learners.fasttext import FasttextLearner
from learners.spacy import SpacyLearner


class TesterProcessor:
    """A TesterProcessor class is in charge of consuming the learning task.

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

        logging.info(f"Consuming a `{task['type']}` task ...")

        # Checks if the task's type is from Spacy
        if task['type'] == 'spacy':
            # Creates a SpacyLearner
            l = SpacyLearner()

        # Checks if the task's type is from Fasttext
        elif task['type'] == 'fasttext':
            # Creates a FasttextLearner
            l = FasttextLearner()

        # Creates a variable with the .zip model's file path
        model_path = os.path.join(c.DEFAULT_PATH, task['id'])

        # If there is no avaliable model
        if not os.path.exists(model_path):
            # Tries to unzip the model
            try:
                # Creates a zipped file path
                model_path_zip = model_path + '.zip'

                # Unzips the model
                model_path = f.unzip_file(model_path_zip, c.DEFAULT_PATH, task['id'])

                logging.info(f'Model unzipped to folder: {model_path}')

            # If file could not be found
            except:
                # Adding an error status to the callback
                task['callback']['status'] = 'error'

                # Notify someone that the model has not been trained (callback)
                logging.info('Sending callback ...')

                raise RuntimeError('Model was not found.')

        # Loads the model
        l.load(model_path)

        # Evaluates the model
        metrics = l.evaluate(task['samples'])

        # Adding metrics to the callback data
        task['callback']['metrics'] = metrics

        # Adding the time when the task has ended
        task['callback']['end_time'] = datetime.datetime.utcnow().isoformat()

        # Adding a success status to the callback
        task['callback']['status'] = 'success'

        logging.debug(f"Task callback: {task['callback']}")

        # Deleting model from disk
        # logging.info('Deleting model from local disk ...')
        # os.remove(model_path)

        # Notify someone that the model has been tested (callback)
        # logging.info('Sending callback ...')
