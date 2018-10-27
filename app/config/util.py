# Standard library
import logging
import os
import sys


_log = logging.getLogger(__name__)


def getenv(key):
    """Gets value of environment variable if found.

    :param key: Name of environment variable.
    :return: Value of environment variable if found.
    """
    try:
        return os.environ[key]
    except KeyError as e:
        _log.error(f'Value for {key} not found')
        sys.exit(1)


def get_database_uri() -> str:
    """Gets database connection uri based on the current APP_PROFILE.

    :return: DB connection string.
    """
    DB_USERNAME = getenv('DB_USERNAME')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_HOST = getenv('DB_HOST')
    DB_PORT = getenv('DB_PORT')
    DB_NAME = getenv('DB_NAME')
    return 'postgresql://{}:{}@{}:{}/{}'.format(
        DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
