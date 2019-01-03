# Standard library
import logging
from typing import Dict, Optional

# 3rd party library
from flask import request

# Internal modules
from app.controllers import util, errors
from app.models import SpamCandidate, ModelType
from app.service import classification_svc
from app.repository import SampleRepo


_log = logging.getLogger(__name__)
_sample_repo = SampleRepo()


def is_spam() -> Dict[str, Optional[str]]:
    """Classifies an incomming text as spam or non-spam.

    :return: Labled SpamCandidate as dict.
    """
    candidate = _get_spam_body()
    _log_request(candidate)
    model_type = _get_model_type()
    candidate.label = classification_svc.classify(candidate.text, model_type)
    _sample_repo.save(candidate)
    return candidate.todict()


def _get_spam_body() -> SpamCandidate:
    """Gets spam candidate from request body.

    :return: SpamCandidate.
    """
    body = util.get_json_body("text")
    return SpamCandidate.fromdict(body)


def _get_model_type() -> ModelType:
    """Gets the model type to be used in classification.

    :return: ModelType
    """
    type_str = util.get_optional_param("model-type", ModelType.SVM.value)
    try:
        return ModelType[type_str]
    except KeyError:
        raise errors.BadRequestError(f"Unkown model type: {type_str}")


def _log_request(candidate: SpamCandidate) -> None:
    """Logs an incomming classification request.

    :param candidate: SpamCandidate
    """
    _log.info(
        f"route: [{request.path}] text: [{candidate.text}] requestId: [{request.id}]"
    )
