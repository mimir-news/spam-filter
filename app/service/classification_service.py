# Standard library
from typing import Optional

# 3rd party modules
from sklearn.pipeline import Pipeline

# Internal modules
from app.config import CASHTAG_THRESHOLD
from app.models import Label, ModelType, SpamResult
from app.repository import ModelRepo
from .training_service import dummy_pipeline


_TOO_MANY_CASHTAGS = "too many cashtags"


class ClassifcationService:
    def __init__(self, model_repo: Optional[ModelRepo]) -> None:
        self._repo = self._get_model_repo(model_repo)

    def classify(self, text: str, model_type: ModelType = ModelType.SVM) -> SpamResult:
        """Classifes a spam candidate.

        :param text: Text to check for indications of spam.
        :param model_type: ModelType to use for classification.
        :return: SpamResult for the tested text.
        """
        if self._to_many_cashtags(text):
            return SpamResult(label=Label.SPAM.value, reason="too many cashtags")
        model = self._repo.get_spam_classifier(model_type)
        return SpamResult(
            label=model.predict([text])[0],
            reason=f"predicted by {model_type.value} model",
        )

    def has_model(self) -> bool:
        """Checks if the services has a trained model.

        :return: Boolen indication if the service has a trained model.
        """
        svm_model = self._repo.get_spam_classifier(ModelType.SVM)
        nb_model = self._repo.get_spam_classifier(ModelType.NAIVE_BAYES)
        return svm_model != None and nb_model != None

    def _to_many_cashtags(self, text: str) -> bool:
        """Check if a given text has to high a cashtag ratio,
        messured as the percentatge of words that are cashtags.

        :param text: Text to test.
        :return: Boolean.
        """
        words = text.split()
        if not words:
            return True
        cashtags = [word for word in words if word.startswith("$")]
        return (len(cashtags) / len(words)) > CASHTAG_THRESHOLD

    def _get_model_repo(self, model_repo: Optional[ModelRepo]) -> ModelRepo:
        """Unpacks an optional ModelRepo.

        :param model_repo: ModelRepo or None
        :return: ModelRepo, either the one supplied as argument or an empyt one.
        """
        if isinstance(model_repo, ModelRepo):
            return model_repo
        empty_repo = ModelRepo(dummy_pipeline(), dummy_pipeline())
        return empty_repo
