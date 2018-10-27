# Standard library
import re
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

# Internal modules
from app import db


class Label(Enum):
    SPAM = 'SPAM'
    NON_SPAM = 'NON-SPAM'


class SpamLabel(db.Model):  # type: ignore
    label: str = db.Column(db.String(10), primary_key=True)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f'SpamLabel(label={self.label} created_at={self.created_at})'


class TrainingData(db.Model):  # type: ignore
    id: int = db.Column(db.Integer, primary_key=True)
    text: str = db.Column(db.String(500))
    label: str = db.Column(db.String(50), db.ForeignKey('spam_label.label'))
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return 'TrainingData(id={} text={} label={} created_at={})'.\
            format(self.id, self.text, self.label, self.created_at)


class SpamCandidate:
    def __init__(self, text: str, label: str = None) -> None:
        self.text = format_text(text)
        self.label = label

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            'text': self.text,
            'label': self.label
        }

    @staticmethod
    def from_dict(raw_dict):
        return SpamCandidate(
            text=raw_dict['text'],
            label=raw_dict['label'] if 'label' in raw_dict else None)


# Regex for identifiying URLs.
_URL_PATTERN = re.compile(r'(https?|ftp):\/\/[\.[a-zA-Z0-9\/\-]+')


def format_text(original: str) -> str:
    """Strips an original string of URLs, double, leading and trailing spaces.

    :param original: String to format.
    :return: Formated string.
    """
    return _URL_PATTERN.sub('', original).replace('  ', ' ').strip().lower()
