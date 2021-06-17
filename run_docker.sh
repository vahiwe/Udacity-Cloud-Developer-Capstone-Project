#!/usr/bin/env bash

## Complete the following steps to get Docker running locally
# Create the following environment variables

# Step 1:
# Build image and add a descriptive tag
docker build --tag=djangoapp \
--build-arg AWS_ACCESS_KEY_ID_ARG=${AWS_ACCESS_KEY_ID_BUCKET} \
--build-arg AWS_SECRET_ACCESS_KEY_ARG=${AWS_SECRET_ACCESS_KEY_BUCKET} \
--build-arg AWS_STORAGE_BUCKET_NAME_ARG=${AWS_STORAGE_BUCKET_NAME} \
--build-arg DEBUG_VALUE_ARG=${DEBUG_VALUE} \
--build-arg DJANGO_KEY_ARG=${DJANGO_KEY} \
--build-arg DATABASE_URL_ARG=${DATABASE_URL} \
--build-arg TWITTER_CONSUMER_KEY_ARG=${TWITTER_CONSUMER_KEY} \
--build-arg TWITTER_CONSUMER_SECRET_ARG=${TWITTER_CONSUMER_SECRET} \
--build-arg TWITTER_ACCESS_TOKEN_ARG=${TWITTER_ACCESS_TOKEN} \
--build-arg TWITTER_ACCESS_SECRET_ARG=${TWITTER_ACCESS_SECRET} .

# Step 2: 
# List docker images
docker image ls

# Step 3: 
# Run Django app
docker run -p 8000:80 djangoapp