# Using an official Python runtime as a parent image
FROM python:3.6-slim

# Gathers list of packages
RUN apt-get update

# Installs G++ for compiling fasttext
RUN apt-get install -y g++

# Creates the application's directory
RUN mkdir -p /brainy

# Sets the work directory to application's folder
WORKDIR /brainy

# Copy files into application's folder
COPY . .

# Copy the host's configuration example as the container's configuration file
COPY config.ini.example config.ini

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Creates the folder for saving models
RUN mkdir -p models

# Execute the application when the container launches
CMD ["python", "api.py"]