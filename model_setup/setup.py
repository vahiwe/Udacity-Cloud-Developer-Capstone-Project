from setuptools import setup, find_packages

setup(
    name='model_setup',
    version='1.0',
    description='Machine Learning Model',
    author='Ahiwe Onyebuchi Valentine',
    author_email='vahiwe@gmail.com',
    packages=find_packages(
        include=['model_setup', 'model_setup.*']),  # same as name
    install_requires=[
        'Django == 2.2.4',
        'Jinja2 >= 2.10.1',
        'matplotlib == 3.0.2',
        'pandas == 0.23.4',
        'numpy == 1.15.4',
        'tweepy == 3.10.0',
        'spacy == 2.1.8',
        'nltk>=3.4.5',
        'scikit-learn == 0.20.2',
        'seaborn == 0.9.0',
        'gunicorn == 19.9.0',
        'python-decouple == 3.4',
        'boto3 == 1.17.93',
        'django-storages == 1.11.1',
        'dj-database-url == 0.5.0',
        'psycopg2 == 2.9',
        'django-annoying == 0.10.6'
    ]
)
