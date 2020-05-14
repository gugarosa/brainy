import logging
import os
import tempfile
import uuid

import fasttext

import utils.constants as c
import utils.file as f
from learners.base_learner import BaseLearner


class FasttextLearner(BaseLearner):
    """A FasttextLearner is in charge of training, evaluating and predicting Fasttext's models.

    """

    def __init__(self):
        """Initialization method.

        """

        # Creating the model's unique identifier
        _id = str(uuid.uuid4())

        # Override its parent class with the receiving parameters
        super(FasttextLearner, self).__init__(id=_id, type='fasttext')

    def _parse(self, samples):
        """It parses an custom input JSON format to Fasttext's format.

        Args:
            samples (list): A list of samples to be parsed.

        Returns:
            A list of tuples already parsed into Fasttext's data format.

        """

        # Creating an empty list to hold the data
        data = []

        # For every possible sample
        for s in samples:
            # Creates an empty list to hold the intents
            intents = ''

            # For every possible intent
            for intent in s['intents']:
                # Appending each intent to an unique string
                intents += '__label__' + intent['label'].lower().strip() + ' '

            # Appends the whole tuple to the data's list
            data.append(intents + s['text'])

        return data

    def _persist(self):
        """Stores the model to the disk.

        Returns:
            The path to the generated zipfile.

        """

        # Creates a temporary directory
        stash_dir = tempfile.TemporaryDirectory()

        # Creates the full path itself
        model_path = os.path.join(c.DEFAULT_PATH, self.id)

        # Saves the model to disk
        self.model.save_model(os.path.join(
            stash_dir.name, c.DEFAULT_FASTTEXT_MODEL))

        # Zips the file
        zip_path = f.zip_file(stash_dir.name, model_path + '.zip', self.id)

        # Cleans up the temporary directory
        stash_dir.cleanup()

        return zip_path

    def _write_file(self, input_data, output_file):
        """Dumps data to a temporary file.

        Args:
            input_data (list): Input data to be dumped.
            output_file (str): Output file to be saved.

        """

        # Gathers all the data into a string
        data = '\n'.join(input_data)

        # Writes the file
        output_file.write(data)

        # Closes the file
        output_file.close()

    def load(self, model_path):
        """Loads a Fasttext's model.

        Args:
            model_path (str): Path of the model to be loaded.

        """

        logging.info(f'Loading model from: {model_path}')

        # Actually loads the model
        self.model = fasttext.load_model(
            os.path.join(model_path, c.DEFAULT_FASTTEXT_MODEL))

    def fit(self, language, samples, hyperparams):
        """Learns a new Intent Classification model through Fasttext.

        Args:
            language (str): The language of the model to be learned.
            samples (list): A list of samples to be learned.
            hyperparams (dict): A dictionary holding all the possible hyperparams.

        Returns:
            The path to the model saved in the local disk.

        """

        # Tries to learn a new model
        try:
            # Parsing samples to Fasttext's format
            train_data = self._parse(samples)

            # Creates a temporary file
            train = tempfile.NamedTemporaryFile(
                'w', delete=False, encoding='utf-8')

            # Dumps the data to a temporary file
            self._write_file(train_data, train)

            # Check if hyperparams are avaliable
            # Checking number of iterations
            if 'n_iterations' not in hyperparams:
                hyperparams['n_iterations'] = 5

            # Checking learning rate
            if 'lr' not in hyperparams:
                hyperparams['lr'] = 0.1

            # Checking word vectors dimension
            if 'dim' not in hyperparams:
                hyperparams['dim'] = 100

            # Checking word n-grams size
            if 'n_grams' not in hyperparams:
                hyperparams['n_grams'] = 1

            # Checking window size
            if 'window_size' not in hyperparams:
                hyperparams['window_size'] = 5

            # Checking loss function
            if 'loss' not in hyperparams:
                hyperparams['loss'] = 'softmax'

            logging.info(f'Training model with: {hyperparams}')

            # Applying hyperparameters to local variables
            epochs = hyperparams['n_iterations']
            lr = hyperparams['lr']
            dim = hyperparams['dim']
            n_grams = hyperparams['n_grams']
            ws = hyperparams['window_size']
            loss = hyperparams['loss']

            # Trains the model
            self.model = fasttext.train_supervised(
                input=train.name, lr=lr, dim=dim, ws=ws, epoch=epochs, wordNgrams=n_grams, loss=loss)

            # Persisting model to disk
            model_path = self._persist()

            logging.info(f'Saving model to: {model_path}')

        # If there is an exception
        except Exception as e:
            # Logs the exception
            logging.exception(e)

            return None

        return model_path

    def evaluate(self, samples):
        """Evaluates a trained model.

        Args:
            samples (list): A list of samples to be evaluated.

        Returns:
            The metrics of the evaluation.

        """

        # Tries to evaluate a trained model
        try:
            # Parsing samples to Fasttext's format
            test_data = self._parse(samples)

            # Creates a temporary file
            test = tempfile.NamedTemporaryFile(
                'w', delete=False, encoding='utf-8')

            # Dumps the data to a temporary file
            self._write_file(test_data, test)

            logging.info('Evaluating model ...')

            # Evaluating model
            m = self.model.test(test.name)

        # If there is an exception
        except Exception as e:
            # Logs the exception
            logging.exception(e)

            return None

        # Creating an object of metrics
        metrics = {
            'n_samples': m[0],
            'precision': m[1],
            'recall': m[2]
        }

        return metrics

    def predict(self, samples):
        """Predicts new samples using the trained model.

        Args:
            samples (list): A list of samples to be predicted.

        Returns:
            An already-structured predictions object.

        """

        logging.info('Performing a new prediction ...')

        # Creates an empty list for the predictions
        preds = []

        # Iterate through every possible sample
        for s in samples:
            # Predicts using the model
            res = self.model.predict(s['text'], k=-1)

            # Creating an empty list of intents
            intents = []

            for i, p in zip(res[0], res[1]):
                # Gathering and formatting the prediction's intent
                intent = i.replace('__label__', '').upper()

                # Gathering and formatting the prediction's intent probability
                prob = p

                # Appending the current intent to the intents list
                intents.append({
                    'label': intent,
                    'probability': prob
                })

            # Appends the prediction to the predictions
            preds.append({
                'text': s['text'],
                'intents': intents
            })

        return preds
