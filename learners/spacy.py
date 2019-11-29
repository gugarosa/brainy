import logging
import os
import random
import tempfile
import uuid

import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer
from spacy.util import compounding, minibatch

import utils.constants as c
import utils.file as f
from learners.base import BaseLearner


class SpacyLearner(BaseLearner):
    """A SpacyLearner is in charge of training, evaluating and predicting Spacy's models.

    """

    def __init__(self):
        """Initialization method.

        """

        # Creating the model's unique identifier
        _id = str(uuid.uuid4())

        # Override its parent class with the receiving parameters
        super(SpacyLearner, self).__init__(id=_id, type='spacy')

    def _parse(self, samples):
        """It parses an custom input JSON format to Spacy's format.

        Args:
            samples (list): A list of samples to be parsed.

        Returns:
            A list of tuples already parsed into Spacy's data format.

        """

        # Creating an empty list to hold the data
        data = []

        # For every possible sample
        for s in samples:
            # Creates an empty list to hold the entities
            entities = []

            # For every possible entity
            for ent in s['entities']:
                # Appends in Spacy's format
                entities.append((ent['start'], ent['end'], ent['label']))

            # Appends the whole tuple to the data's list
            data.append((s['text'], {'entities': entities}))

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
        self.model.to_disk(stash_dir.name)

        # Zips the file
        zip_path = f.zip_file(stash_dir.name, model_path + '.zip', self.id)

        # Cleans up the temporary directory
        stash_dir.cleanup()

        return zip_path

    def load(self, model_path):
        """Loads a Spacy's model.

        Args:
            model_path (str): Path of the model to be loaded.

        """

        logging.info(f'Loading model from: {model_path}')

        # Actually loads the model
        self.model = spacy.load(model_path)

    def fit(self, language, samples, hyperparams):
        """Learns a new Named Entity Recognition model through Spacy.

        Args:
            language (str): The language of the model to be learned.
            samples (list): A list of samples to be learned.
            hyperparams (dict): A dictionary holding all the possible hyperparams.

        Returns:
            The path to the model saved in the local disk.

        """

        # Tries to learn a new model
        try:
            # Creating a blank model
            self.model = spacy.blank(language)

            # Creating a NER pipeline
            ner = self.model.create_pipe('ner')

            # Adding the pipeline to the model itself
            self.model.add_pipe(ner, last=True)

            # Parsing samples to Spacy's format
            train_data = self._parse(samples)

            # For each possible example in the data
            for _, d in train_data:
                # For each possible entity in the sample
                for ent in d.get('entities'):
                    # Adds its corresponding label
                    ner.add_label(ent[2])

            # Check if hyperparams are avaliable
            # Checking number of iterations
            if 'n_iterations' not in hyperparams:
                hyperparams['n_iterations'] = 100

            # Checking dropout
            if 'dropout' not in hyperparams:
                hyperparams['dropout'] = 0.5

            # Checking learning rate
            if 'lr' not in hyperparams:
                hyperparams['lr'] = 0.001

            # Checking batch size
            if 'batch_size' not in hyperparams:
                hyperparams['batch_size'] = 32

            logging.info(f'Training model with: {hyperparams}')

            # Starts the training
            optimizer = self.model.begin_training()

            # Applying new hyperparams
            optimizer.alpha = hyperparams['lr']

            # For each iteration
            for t in range(hyperparams['n_iterations']):
                logging.debug(f"Iteration {t+1}/{hyperparams['n_iterations']}")

                # Randomize the training data
                random.shuffle(train_data)

                # Creates an empty dictionary to hold the losses
                loss = {}

                # Creates the minibatches
                batches = minibatch(train_data, size=compounding(
                    4.0, hyperparams['batch_size'], 1.001))

                # For every batch
                for batch in batches:
                    # Zips the batch with texts and labels
                    texts, labels = zip(*batch)

                    # Updates the model
                    self.model.update(
                        texts, labels, drop=hyperparams['dropout'], sgd=optimizer, losses=loss)

                logging.debug(f"Loss: {loss['ner']}")

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

        # Tries to learn a new model
        try:
            # Parsing samples to Spacy's format
            test_data = self._parse(samples)

            # Creates a scorer object
            scorer = Scorer()

            # For each sample in the testing data
            for text, label in test_data:
                # Creates a GoldParse object with the correct annotation
                correct = GoldParse(self.model.make_doc(
                    text), entities=label['entities'])

                # Calculates the prediction
                pred = self.model(text)

                # Evaluates the prediction according to correct label
                scorer.score(pred, correct)

        # If there is an exception
        except Exception as e:
            # Logs the exception
            logging.exception(e)

            return None

        # Outputs the scorer metrics to a specific variable
        metrics = scorer.scores

        return metrics

    def predict(self, samples):
        """Predicts new samples using the pre-trained model.

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
            res = self.model(s['text'])

            # Creates an empty list for the entities
            entities = []

            # Creates a list of every possible predicted entity
            for e in res.ents:
                # Appends a new object with the entity structure
                entities.append({
                    'value': e.text,
                    'start': e.start_char,
                    'end': e.end_char,
                    'label': e.label_
                })

            # Appends the entities to the prediction
            preds.append({
                'text': s['text'],
                'entities': entities
            })

        return preds
