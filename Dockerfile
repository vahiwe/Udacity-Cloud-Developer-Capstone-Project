# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Add Arguments
ARG AWS_ACCESS_KEY_ID_ARG
ARG AWS_SECRET_ACCESS_KEY_ARG
ARG AWS_STORAGE_BUCKET_NAME_ARG
ARG DEBUG_VALUE_ARG
ARG DJANGO_KEY_ARG
ARG TWITTER_CONSUMER_KEY_ARG
ARG TWITTER_CONSUMER_SECRET_ARG
ARG TWITTER_ACCESS_TOKEN_ARG
ARG TWITTER_ACCESS_SECRET_ARG

# Set Environment Variable
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID_ARG}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY_ARG}
ENV AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME_ARG}
ENV DEBUG_VALUE=${DEBUG_VALUE_ARG}
ENV DJANGO_KEY=${DJANGO_KEY_ARG}
ENV TWITTER_CONSUMER_KEY=${TWITTER_CONSUMER_KEY_ARG}
ENV TWITTER_CONSUMER_SECRET=${TWITTER_CONSUMER_SECRET_ARG}
ENV TWITTER_ACCESS_TOKEN=${TWITTER_ACCESS_TOKEN_ARG}
ENV TWITTER_ACCESS_SECRET=${TWITTER_ACCESS_SECRET_ARG}

# create root directory for our project in the container
RUN mkdir /TwitterAnalysis

# Copy the current directory contents into the container at /TwitterAnalysis
ADD . /TwitterAnalysis/

# Set the working directory to /TwitterAnalysis/model_setup
WORKDIR /TwitterAnalysis/model_setup

# Install any needed packages specified in setup.py
RUN pip install -e .

# Set the working directory to /TwitterAnalysis/model_setup
WORKDIR /TwitterAnalysis

# Install spacy language model
RUN python -m spacy download en

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container using Django
# Uncomment the next two lines to use django to render app and comment gunicorn command
# ENTRYPOINT ["python", "manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]

# define the default command to run when starting the container using gunicorn
CMD ["gunicorn", "--bind", ":8000", "TwitterAnalysis.wsgi:application"]