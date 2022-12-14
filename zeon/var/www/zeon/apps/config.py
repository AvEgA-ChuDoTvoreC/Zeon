# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""

import os
from decouple import config


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set logging level
    LOGGING_LEVEL = config('LOGGING_LEVEL', default='DEBUG')

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = (
        '{dialect}+{driver}://{user}:{password}@{host}:{port}/{db_name}'.format(
            dialect=config('DB_ENGINE', default='postgresql'),
            driver=config('DB_DRIVER', default='psycopg2'),
            user=config('DB_USER', default='neo'),
            password=config('DB_PASS', default='123qweasd'),
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default=5432),
            db_name=config('DB_NAME', default='zeon'))
    )


class DebugConfig(Config):
    DEBUG = True

    # print SQL queries to DB, generated by SQLAlchemy
    # SQLALCHEMY_ECHO = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
