import logging

import spacy


def learn(samples, hyperparams):
    """
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

    return nlp
