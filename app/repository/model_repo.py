# Standard libarary
import logging

# 3rd party modules
from sklearn.pipeline import Pipeline

# Internal modules
from app import db
from app.models import Classifier, ModelType


class ModelRepo:

    __log = logging.getLogger('ModelRepo')

    def __init__(self, svm_model: Pipeline, nb_model: Pipeline) -> None:
        self.__models = {
            ModelType.SVM: svm_model,
            ModelType.NAIVE_BAYES: nb_model
        }

    def get_spam_classifier(self, type: ModelType = ModelType.SVM) -> Pipeline:
        """Gets spam classification model.

        :param type: Model type to use.
        :return: Spam classification model.
        """
        return self.__models[type]

    def save_classifier(self, classifier: Classifier) -> None:
        """Saves a classifier in the database.

        :param classifier: Classifier to save
        """
        if self.__classifier_exists(classifier):
            self.__log.info(f'Classifier with hash {classifier.model_hash} already exists')
            return
        db.session.add(classifier)
        db.session.commit()

    def __classifier_exists(self, classifier: Classifier) -> bool:
        existing_classifiers = Classifier.query.\
            filter(Classifier.model_hash == classifier.model_hash).all()
        return len(existing_classifiers) > 0
