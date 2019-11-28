import logging
import os
import random
import tempfile

import spacy
from spacy.util import compounding, minibatch

import utils.file as f


def _parse_samples(samples):
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


def _persist(path, _id, model):
    """Stores the model to the disk.

    Args:
        path (str): Folder where the zipfile will be created.
        _id (str): Model's identifier.
        model (Spacy): Model's object.

    Returns:
        The path to the generated zipfile.

    """

    # Creates a temporary directory
    stash_dir = tempfile.TemporaryDirectory()

    # Creates the full path itself
    model_path = os.path.join(path, _id)

    # Saves the model to disk
    model.to_disk(stash_dir.name)

    # Zips the file
    zip_path = f.zip_file(stash_dir.name, model_path + '.zip', _id)

    # Cleans up the temporary directory
    stash_dir.cleanup()

    return zip_path


def learn(language, samples, hyperparams):
    """Learns a new Named Entity Recognition Model through Spacy.

    Args:
        language (str): The language of the model to be learned.
        samples (list): A list of samples to be learned.
        hyperparams (dict): A dictionary holding all the possible hyperparams.

    Returns:
        The path to the model saved in the local disk.

    """

    logging.info(f'Creating a blank `{language}` model ...')

    # Creating a blank model
    nlp = spacy.blank(language)

    logging.info('Adding NER to model pipeline ...')

    # Creating a NER pipeline
    ner = nlp.create_pipe('ner')

    # Adding the pipeline to the model itself
    nlp.add_pipe(ner, last=True)

    logging.info('Parsing samples to Spacy data structure ...')

    # Parsing samples to Spacy's format
    train_data = _parse_samples(samples)

    logging.info('Adding entities to the model ...')

    # For each possible example in the data
    for _, d in train_data:
        # For each possible entity in the sample
        for ent in d.get('entities'):
            # Adds its corresponding label
            ner.add_label(ent[2])

    logging.info(f'Training model with: {hyperparams}')

    # Starts the training
    nlp.begin_training()

    # For each iteration
    for t in range(hyperparams['n_iterations']):
        logging.debug(f"Iteration {t+1}/{hyperparams['n_iterations']}")

        # Randomize the training data
        random.shuffle(train_data)

        # Creates an empty dictionary to hold the losses
        loss = {}

        # Creates the minibatches
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))

        # For every batch
        for batch in batches:
            # Zips the batch with texts and labels
            texts, labels = zip(*batch)

            # Updates the model
            nlp.update(texts, labels, drop=0.5, losses=loss)

        logging.debug(f"Loss: {loss['ner']}")

    logging.info('Saving model into local disk ...')

    # Persisting model to disk
    model_path = _persist('models/', '1', nlp)

    logging.info(f'Model saved to: {model_path}')

    return model_path
