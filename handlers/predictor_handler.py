import logging
import os

import tornado

import utils.constants as c
import utils.file as f
from handlers.base_handler import BaseHandler
from learners.fasttext_learner import FasttextLearner
from learners.spacy_learner import SpacyLearner


class PredictorHandler(BaseHandler):
    """A PredictorHandler defines all possible methods for predicting a model.

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

        # Getting request object
        req = tornado.escape.json_decode(self.request.body)

        # Gathering the model's identifier
        _id = req['id']

        # Gathering the model's type
        _type = req['type']

        # Gathering the samples
        samples = req['samples']

        # Creates a variable with the .zip model's file path
        model_path = os.path.join(c.DEFAULT_PATH, _id)

        # If there is no avaliable model
        if not os.path.exists(model_path):
            # Tries to unzip the model
            try:
                # Creates a zipped file path
                model_path_zip = model_path + '.zip'

                # Unzips the model
                model_path = f.unzip_file(model_path_zip, c.DEFAULT_PATH, _id)

                logging.info(f'Model unzipped to folder: {model_path}')

            except FileNotFoundError:
                logging.error(f'Could not find {model_path_zip}')

                # Returns an error
                self.set_status(500)

                # Writing back an error message
                self.finish(
                    dict(error='There is no avaliable model with such identifier.'))

                return False

        # Checks if the learner's type is from Spacy
        if _type == 'spacy':
            # If yes, creates a SpacyLearner
            l = SpacyLearner()

        # Checks if the learner's type is from Fasttext
        elif _type == 'fasttext':
            # If yes, creates a FasttextLearner
            l = FasttextLearner()

        # Loads the model
        l.load(model_path)

        # Tries to perform the prediction
        try:
            # Actually performs the prediction
            preds = l.predict(samples)

        # If prediction could not be realized, reply with an error
        except Exception as e:
            logging.exception(e)

            # Setting status to error
            self.set_status(500)

            # Writing back an error message
            self.finish(dict(error='Failed to perform a new prediction.'))

            return False

        # Writing back the predictions
        self.finish(dict(predictions=preds))

        return True
