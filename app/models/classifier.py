# Standard library
from datetime import datetime
from enum import Enum

# Internal modules
from app import db

class ModelType(Enum):
    SVM = 'SVM'
    NAIVE_BAYES = 'NAIVE-BAYES'


class Classifier(db.Model):  # type: ignore
    id: int = db.Column(db.Integer, primary_key=True)
    type: str = db.Column(db.String(50))
    training_samples: int = db.Column(db.Integer, nullable=False)
    test_samples: int = db.Column(db.Integer, nullable=False)
    accuracy: float = db.Column(db.Float, nullable=False)
    model_hash: str = db.Column(db.String(64))
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return ('Classifier(id={} type={} training_samples={} '
                'test_samples={} accuracy={} model_hash={} '
                'created_at={})').format(
                    self.id, self.type, self.training_samples,
                    self.test_samples, self.accuracy, self.model_hash,
                    self.created_at)
