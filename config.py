import os
import re
from flask import config

envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')
print("Importing variables from .env file")
try:
    with open('config.env') as ins:
        for line in ins:
            match = envre.match(line)
            if match is not None:
                os.environ[match.group(1)] = match.group(2)
except EnvironmentError:
    print("It seems someone forgot to add config.env file")

class BaseConfig:
    CACHE_TYPE = os.environ.get('CACHE_TYPE')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT')
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')

    @staticmethod
    def init_app(app):
        pass

class DevConfig(BaseConfig):
    DEBUG = True
    ASSETS_DEBUG = True

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE.')

        
class ProdConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY') if os.environ.get('SECRET_KEY') else None

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        assert os.environ.get('SECRET_KEY'), None


config = {
    'dev': DevConfig,
    'prod': ProdConfig
}