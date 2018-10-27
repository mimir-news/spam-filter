# Standard library
from abc import ABCMeta, abstractmethod
from typing import List

# 3rd party modules
from sqlalchemy import desc

# Internal modules
from app import db
from app.models import TrainingData


class TrainingDataRepo:

    def save(self, training_data: TrainingData) -> None:
        """Stores a new training data sample in the database.

        :param training_data: TrainingData sample to store.
        """
        db.session.add(training_data)
        db.session.commit()

    def get_all(self) -> List[TrainingData]:
        """Gets spam classification model.

        :return: List of training data.
        """
        return TrainingData.query.order_by(desc(TrainingData.created_at))
