# Standard library
import logging
from typing import Dict, Optional

# Internal modules
from app.controllers import util, errors
from app.models import SpamCandidate, ModelType
from app.service import classification_svc


_log = logging.getLogger(__name__)


def is_spam() -> Dict[str, Optional[str]]:
    """Classifies an incomming text as spam or non-spam.

    :return: Labled SpamCandidate as dict.
    """
    candidate = _get_spam_body()
    model_type = _get_model_type()
    candidate.label = classification_svc.classify(candidate.text, model_type)
    return candidate.to_dict()


def _get_spam_body() -> SpamCandidate:
    """Gets spam candidate from request body.

    :return: SpamCandidate.
    """
    body = util.get_json_body('text')
    return SpamCandidate.from_dict(body)


def _get_model_type() -> ModelType:
    """Gets the model type to be used in classification.

    :return: ModelType
    """
    type_str = util.get_optional_param('model-type', ModelType.SVM.value)
    try:
        return ModelType[type_str]
    except KeyError as e:
        raise errors.BadRequestError(f'Unkown model type: {type_str}')
