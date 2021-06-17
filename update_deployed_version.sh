#!/bin/bash

sed -i "s/VERSION/${TRAVIS_BUILD_NUMBER}/g" K8s/twitter-analysis-deployment.yaml

sed -i "s/VERSION/${TRAVIS_BUILD_NUMBER}/g" K8s/reverse-proxy-deployment.yaml

echo "Version updated"