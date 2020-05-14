class BaseLearner:
    """A BaseLearner class is in charge of defining the basic methods
        that a child learner should implement.

    """

    def __init__(self, id=None, type=None):
        """Initialization method.

        Args:
            id (str): The learner's identifier.
            type (str): The learner's type.

        """

        # Learner's identifier
        self.id = id

        # Learner's type
        self.type = type

        # Learner's model instance
        self.model = None

    def _parse(self, samples):
        """It parses an custom input JSON format to the learner's data format.

        Args:
            samples (list): A list of samples to be parsed.

        Returns:
            It should return the parsed data into the learner's data format.

        """

        raise NotImplementedError(
            'The method `_parse` should be implemented in the child.')

    def _persist(self):
        """Stores the model to the disk.

        Returns:
            It should return the path to the generated .zip.

        """

        raise NotImplementedError(
            'The method `_persist` should be implemented in the child.')

    def load(self, model_path):
        """Loads a new learner.

        Args:
            model_path (str): Path of the model to be loaded.

        """

        raise NotImplementedError(
            'The method `load` should be implemented in the child.')

    def fit(self, language, samples, hyperparams):
        """Fits a new learner.

        Args:
            language (str): The language of the model to be learned.
            samples (list): A list of samples to be learned.
            hyperparams (dict): A dictionary holding all the possible hyperparams.

        Returns:
            It should return the path to the learner saved in the local disk.

        """

        raise NotImplementedError(
            'The method `fit` should be implemented in the child.')

    def evaluate(self, samples):
        """Evaluates a trained learner.

        Args:
            samples (list): A list of samples to be evaluated.

        Returns:
            It should return the metrics of the evaluation.

        """

        raise NotImplementedError(
            'The method `evaluate` should be implemented in the child.')

    def predict(self, samples):
        """Predicts new inputs using a trained learner.

        Args:
            samples (list): A list of samples to be predicted.

        Returns:
            It should return an already-structured predictions object.

        """

        raise NotImplementedError(
            'The method `predict` should be implemented in the child.')
