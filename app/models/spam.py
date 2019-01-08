# Standard library
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

# Internal modules
from app import db


class Label(Enum):
    SPAM = "SPAM"
    NON_SPAM = "NON-SPAM"


class SpamLabel(db.Model):  # type: ignore
    label: str = db.Column(db.String(10), primary_key=True)
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"SpamLabel(label={self.label} created_at={self.created_at})"


class TrainingData(db.Model):  # type: ignore
    id: int = db.Column(db.Integer, primary_key=True)
    text: str = db.Column(db.String(500))
    label: str = db.Column(db.String(50), db.ForeignKey("spam_label.label"))
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return "TrainingData(id={} text={} label={} created_at={})".format(
            self.id, self.text, self.label, self.created_at
        )


class SpamCandidate:
    def __init__(self, text: str, label: str = None) -> None:
        self.text = format_text(text)
        self.label = label

    def todict(self) -> Dict[str, Optional[str]]:
        return {"text": self.text, "label": self.label}

    @classmethod
    def fromdict(cls, raw) -> "SpamCandidate":
        return cls(text=raw["text"], label=raw["label"] if "label" in raw else None)


@dataclass(frozen=True)
class SpamResult:
    label: str
    reason: str

    def todict(self) -> Dict[str, str]:
        return {"label": self.label, "reason": self.reason}


class ResultSample(db.Model):  # type: ignore
    id: int = db.Column(db.Integer, primary_key=True)
    text: str = db.Column(db.String(500))
    label: str = db.Column(db.String(50))
    reason: str = db.Column(db.String(50))
    is_confirmed: bool = db.Column(db.Boolean, default=False)
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )

    @classmethod
    def from_candidate(cls, candidate: SpamCandidate) -> "ResultSample":
        return cls(text=candidate.text, label=candidate.label)

    @classmethod
    def from_result(cls, res: SpamResult, text: str) -> "ResultSample":
        return cls(text=text, label=res.label, reason=res.reason)

    def __repr__(self) -> str:
        return "ResultSample(id={} text={} label={} reason={} is_confirmed={} created_at={})".format(
            self.id,
            self.text,
            self.label,
            self.reason,
            self.is_confirmed,
            self.created_at,
        )


# Regex for identifiying URLs.
_URL_PATTERN = re.compile(r"(https?|ftp):\/\/[\.[a-zA-Z0-9\/\-]+")


def format_text(original: str) -> str:
    """Strips an original string of URLs, double, leading and trailing spaces.

    :param original: String to format.
    :return: Formated string.
    """
    return _URL_PATTERN.sub("", original).replace("  ", " ").strip().lower()
