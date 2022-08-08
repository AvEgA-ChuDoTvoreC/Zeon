# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""

from flask import Flask
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()
# login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    # login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('api', ):    # Register New App here
        module = import_module('apps.{}.routes'.format(module_name))  # Check this out at core.utils.module_lloading
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logger(config):
    """
    CRITICAL 50
    ERROR    40
    WARNING  30
    INFO     20
    DEBUG    10
    NOTSET   0
    """
    import logging
    # from logging.handlers import TimedRotatingFileHandler
    logging.basicConfig(
        # handlers=[TimedRotatingFileHandler('ff.log', when="midnight")],
        level=config.LOGGING_LEVEL,
        format='[%(asctime)s] : [%(levelname)-8s] : [%(filename)s.%(lineno)s] :: %(message)s',
    )


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logger(config)
    return app
