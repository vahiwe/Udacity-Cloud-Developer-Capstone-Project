#!/bin/bash

docker build -t vahiwe/twitteranalysis:$TRAVIS_BUILD_NUMBER \
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

docker build -t vahiwe/simple-reverse-proxy:$TRAVIS_BUILD_NUMBER -f ./reverse-proxy/Dockerfile ./reverse-proxy/

echo "Image built successfully"