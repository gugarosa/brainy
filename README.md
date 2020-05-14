# Brainy

## Welcome to Brainy.

This is an easy-to-use solution for training, testing, and predicting models on-demand. Brainy offers a high-level API where requests can be made via JSON in order to train an NLP-based model. Additionally, after the model has been trained and persisted on disk, it is possible to be further loaded and used for new predictions and tests. Please, follow along the next sections in order to learn more about this excellent tool.

Brainy is compatible with: **Python 3.6+**.

---

## Package guidelines

1. The very first information you need is in the very **next** section.
2. **Installing** is also easy if you wish to read the code and bump yourself into, follow along.
3. Note that there might be some **additional** steps in order to use our solutions.
4. If there is a problem, please do not **hesitate**. Call us.

---

## Getting started: 60 seconds with Brainy

First of all. Code is commented. Yes, everything is commented. Just browse to any file, chose your subpackage, and follow it. We have high-level code for most tasks we could think.

Alternatively, if you wish to learn even more, please take a minute:

Brainy is based on the following structure, and you should pay attention to its tree:

```
- brainy
    - handlers
        - base_handler
        - predictor_handler
        - tester_handler
        - trainer_handler
    - learners
        - base_learner
        - fasttext_learner
        - spacy_learner
    - postman
    - processors
        - tester_processor
        - trainer_processor
    - utils
        - constants
        - file
        - process_manager
        - server
```

### Handlers

This package should handle any route that needs to be used within this API.

### Learners

One can define a custom learner or use the pre-defined ones. The learner stands for the machine learning toolkit or algorithm used to perform the training, testing and prediction processes.

### Postman

This package provides a collection of possible requests that are available within this API.

### Processors

The processors are responsible for invoking and consuming the task queues, providing a callback when the task has been invoked, consumed, and finished.

### Utils

A utilities package stands for common things shared across the application. It is better to implement once and use it as you wish than re-implementing the same thing over and over again.

---

## Installation

We believe that everything has to be easy. Not tricky or daunting, Brainy will be the one-to-go package that you will need, from the very first installation to the daily-tasks implementing needs.

Remember that you need to adjust `config.ini.example` according to your needs and to make sure that `docker` or `docker-compose` are installed and accessible from the command line.

### Docker

First of all, you need to build the container's image, as follows:

```
docker build --tag brainy .
```

After building it, it is now possible to run with the following command:

```
docker run -p 8080:8080 --name brainy brainy:latest
```

Note that we are assuming that the API uses port 8080 and that this port will be mapped as 8080 in the host.


### Docker-Compose

First of all, you need to build the container's image, as follows:

```
docker-compose build
```

After the build process is finished, you can run the container in detached mode:

```
docker-compose up -d
```

If you ever need to perform maintenance or update the repository, please put the container down:

```
docker-compose down
```

---

## Environment configuration

Note that sometimes, there is a need for additional implementation. If needed, from here, you will be the one to know all of its details.

### Ubuntu

No specific additional commands needed.

### Windows

No specific additional commands needed.

### MacOS

No specific additional commands needed.

---

## Support

We know that we do our best, but it is inevitable to acknowledge that we make mistakes. If you ever need to report a bug, report a problem, talk to us, please do so! We will be available at our bests at this repository or gustavo.rosa@unesp.br.

---
