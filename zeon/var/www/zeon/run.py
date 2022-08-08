# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""

from flasgger import Swagger
from flask_migrate import Migrate
from sys import exit
from decouple import config
from flask import abort
from sqlalchemy.exc import OperationalError

from apps.config import config_dict
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)
Swagger(app)


@app.before_request
def check_db_connection():
    __doc__ = """
        Test DataBase connection before proceed"""

    try:
        db.engine.connect()
    except OperationalError as exc_info:
        app.logger.error('Нет соединения с базой данных. {}.'.format(exc_info))
        abort(500)


@app.errorhandler(500)
def internal_server_error(err):
    __doc__ = """
        Catch 500 Error on the app level"""
    app.logger.error(err)
    return dict(message='Внутренняя ошибка сервера'), err.code


# TODO: add health-check for subsystems: Zabbix, XmlParser
if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
