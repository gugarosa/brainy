import logging
import spacy


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

        logging.info('Creating a blank model ...')

        #
        nlp = spacy.blank('pt')

        logging.info('Adding NER to model pipeline ...')

        #
        if 'ner' not in nlp.pipe_names:
            #
            ner = nlp.create_pipe('ner')
            
            #
            nlp.add_pipe(ner, last=True)
        
        else:
            #
            ner = nlp.get_pipe('ner')
