# Standard library
import logging
from typing import Any, Dict

# Internal modules
from app.controllers import util, errors
from app.models import ModelType, TrainingData, Label
from app.repository import TrainingDataRepo


__training_data_repo = TrainingDataRepo()


_log = logging.getLogger(__name__)


def add_training_data() -> None:
    """Adds new training if correctly formated."""
    body = util.get_json_body('text', 'label')
    training_data = _parse_training_data(body)
    __training_data_repo.save(training_data)


def _parse_training_data(body: Dict[str, Any]) -> TrainingData:
    """Parses request body into training data if the data is correct.

    :param body: Raw request body as dict.
    :return: TrainingData.
    """
    return TrainingData(
        text=body['text'],
        label=_parse_spam_label(body['label']).value)


def _parse_spam_label(label: str) -> Label:
    """Parses a label text into a correct Label if possible.

    :param label: Spam label as string.
    :return: Label.
    """
    formated_label = label.upper().replace('-', '_')
    try:
        return Label[formated_label]
    except KeyError:
        raise errors.BadRequestError(f'Unsupported label: {label}')
