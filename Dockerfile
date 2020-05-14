# Using an official Python runtime as a parent image
FROM python:3.6-slim

# Gathers list of packages
# RUN apt-get update

# Installs GCC for compiling fasttext
# RUN apt-get install -y gcc

# Creates the application's directory
RUN mkdir -p /brainy

# Sets the work directory to application's folder
WORKDIR /brainy

# Copy files into application's folder
COPY . .

# Copy the local configuration example as the host's configuration file
COPY config.ini.example config.ini

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Execute the application when the container launches
CMD ["python", "api.py"]