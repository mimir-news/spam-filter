# Standard library
import logging
from typing import Dict, List, Tuple

# Internal modules
from app import db
from app.controllers import status
from app.service import classification_svc


_log = logging.getLogger(__name__)


STATUS_UP: str = 'UP'
STATUS_DOWN: str = 'DOWN'


def check_health() -> Tuple[Dict[str, str], int]:
    """Handles health check requests.

    :return: Status info as a dict.
    :return: HTTP status code.
    """
    db_status, db_ok = _check_db_status()
    model_status, model_ok = _check_model_status()
    overall_status, status_code = _determine_overall_status(model_ok, db_ok)
    health_info = {
        'status': overall_status,
        'model': model_status,
        'db': db_status
    }
    return health_info, status_code


def _check_model_status() -> Tuple[str, bool]:
    """Checks that the spam filter model is trained
    and ready to classify requests

    :return: Status text.
    :return: Boolean indication if status is healthy
    """
    model_ok = classification_svc.has_model()
    return STATUS_UP if model_ok else STATUS_DOWN, model_ok


def _check_db_status() -> Tuple[str, bool]:
    """Pings the database to check if the service is connetcted.

    :return: Status text.
    :return: Boolean indication if status is healthy
    """
    try:
        db.engine.execute('SELECT 1')
        return 'UP', True
    except Exception as e:
        _log.error(str(e))
        return 'DOWN', False


def _determine_overall_status(*statuses: bool) -> Tuple[str, int]:
    """Checks that all statuses entered are true for healthy.

    :param statuses: List of booelans indicating individual components health.
    :return: Status description as a string
    :return: Status code.
    """
    if all(statuses):
        return STATUS_UP, status.HTTP_200_OK
    return STATUS_DOWN, status.HTTP_503_SERVICE_UNAVAILIBLE
