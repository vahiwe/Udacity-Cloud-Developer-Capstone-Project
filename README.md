# Capstone Project for Udacity Cloud Developer Nanodegree

This project fulfills the requirements of the Udacity Cloud Developer Capstone Project. A web app is containerized and deployed to a kubernetes cluster. This webapp runs a sentiment analysis on tweets of a Twitter handle and gives feedback on sentiments over a period of time.

## :page_with_curl:  _Information on Some of the files_

**1)** `build_images.sh` - This file contains the shell commands needed to build the image using docker.

**2)** `K8s/` - This folder contains the kubernetes resource configuration files that will deploy the application image on AWS EKS using `kubectl` once configured properly.

**3)** `Dockerfile` - This file contains all the commands needed to assemble the app image.

**4)** `update_deployed_version.sh` - This file uses the command line tool 'sed' in updating the kubernetes configuration file in other to force the pods to update with the new image. The reason for this is that Kubernetes (wrongly) considers Docker tags as immutable (i.e., once a tag is set, it is never changed). The rolling update is also activated by the change in image name.   

**5)** `.travis.yml` - This file contains the commands for Travis to handle CI/CD process of the application.

## :page_with_curl:  _Local Docker Setup_

To run this app using docker, a script has been attached that builds an image from the Dockerfile and spins up a container running the web app:

__`❍ ./run_docker.sh `__

There is also a script that uploads the Docker image to a designated repo. This should be edited before execution:

__`❍ ./upload_docker.sh `__

Please view the aforementioned scripts before running to understand the logic behind them.

## :page_with_curl:  _Setup Instructions for local testing_

**1)** Fire up your favourite console & clone this repo somewhere:

__`❍ git clone https://github.com/vahiwe/TwitterAnalysis.git`__

**2)** Enter this directory:

__`❍ cd TwitterAnalysis/model_setup`__

**3)** Install [python](https://www.python.org/) if not already installed and run this command to install python packages/dependencies:

__`❍ pip install -e . `__

**4)** Go back to previous directory:

__`❍ cd .. `__

**5)** Generate secret key for Django project [here](https://miniwebtool.com/django-secret-key-generator/) and create this environment variable. There is a default `DJANGO_KEY` already set in the project:

``` 
    export DJANGO_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**6)** Get your [Twitter Developer](https://developer.twitter.com/) credentials and create the following environment variables :
```
    export TWITTER_CONSUMER_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 
    export TWITTER_CONSUMER_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    export TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    export TWITTER_ACCESS_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**7)** If you need to serve static files from an S3 bucket, you can set the following environment variables. The credentials should have permissions to perform the operations listed [here](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#iam-policy) on the S3 Bucket:

``` 
    export DEBUG_VALUE=False
    export AWS_STORAGE_BUCKET_NAME=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    export AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**8)** If you would like to use a database in storing the tweets and feedback data, you can set the following environment variables:

``` 
    export DATABASE_URL=postgres://dbuser:dbpassword@hostname:5432/dbname
```

**9)** Install spacy language model:

__`❍ python -m spacy download en `__

**10)** Run to create migrations for changes:

__`❍ python manage.py makemigrations`__

**11)** Run to apply those changes to the database:

__`❍ python manage.py migrate`__

**12)** Start the server to view the webapp:

__`❍ python manage.py runserver `__

**13)** Open your browser and type in this URL to view the webapp:

__`❍ http://127.0.0.1:8000/`__

__*Happy developing!*__
