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
    APP_NAME = os.environ.get('APP_NAME') or 'Flask-Base'
    SECRET_KEY = os.environ.get('SECRET_KEY') if os.environ.get('SECRET_KEY') else None

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

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        assert os.environ.get('SECRET_KEY'), None


config = {
    'dev': DevConfig,
    'prod': ProdConfig
}