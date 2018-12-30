# Standard library
import os
from logging.config import dictConfig

# Setup of logging configureaion
from .logging import LOGGING_CONIFG
dictConfig(LOGGING_CONIFG)

# Internal modultes
from app.config import util


CASHTAG_THRESHOLD: float = float(os.getenv("CASHTAG_THRESHOLD", "0.8"))
TRAIN_MODEL: bool = os.getenv("TRAIN_MODEL", "TRUE") == "TRUE"
REQUEST_ID_HEADER = "X-Request-ID"
SERVICE_NAME: str = os.getenv("SERVICE_NAME", "spam-filter")
SERVICE_VERSION: str = os.getenv("SERVICE_VERSION", "2.2")
SERVER_NAME: str = f"{SERVICE_NAME} {SERVICE_VERSION}"


class AppConfig:
    SQLALCHEMY_DATABASE_URI: str = util.get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
