# Standard library
import logging
import sys
from random import random

# Internal modules
from app import db
from app.config import RESULT_SAMPLE_RATE
from app.models import SpamResult, ResultSample


class SampleRepo:

    _log = logging.getLogger("")

    def __init__(self):
        self._sample_rate: float = RESULT_SAMPLE_RATE
        if self._sample_rate > 1.0:
            self._log.error(f"Sample rate is {self._sample_rate}. Max is 1.0")
            sys.exit(1)

    def save(self, res: SpamResult, text: str) -> None:
        """Optionaly adds a classified sample derived from a candidate.

        :param res: SpamResult to convert.
        :param text: Classified text.
        """
        if self._should_sample():
            sample = ResultSample.from_result(res, text)
            db.session.add(sample)
            db.session.commit()

    def _should_sample(self) -> bool:
        """Determines if a sample should be created and saved.

        :return: Boolean
        """
        return random() < self._sample_rate

