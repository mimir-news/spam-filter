# Standard library
import logging
import re
from collections import namedtuple
from hashlib import sha1
from typing import Iterable, Tuple

# Internal modules
from app.models import Classifier, ModelType, TrainingData
from app.repository import TrainingDataRepo

# 3rd party library
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from stop_words import get_stop_words


DataList = namedtuple('DataList', ['texts', 'labels'])


class TrainingService:

    __log = logging.getLogger('TrainingServiceImpl')

    def __init__(self, sample_repo: TrainingDataRepo) -> None:
        self.__sample_repo = sample_repo

    def train_model(self, type: ModelType) -> Tuple[Pipeline, Classifier]:
        """Retrieves training data and creates a model.

        :param type: Type of model to train.
        :return: Trained model.
        :return: Classifier metadata.
        """
        training_data, test_data = self.__get_and_split_data()
        model = self.__init_model(type)
        model.fit(training_data.texts, training_data.labels)
        metadata = self.__create_metadata(model, type, training_data, test_data)
        return model, metadata

    def __init_svm_model(self) -> Pipeline:
        """Initalizes an untrained Support Vector Machine model.

        :return: Sklearn Pipeline with vectorization and prediction model.
        """
        return Pipeline([
            ('counter', CountVectorizer(stop_words=get_stop_words('english'))),
            ('tfidf', TfidfTransformer()),
            ('classifier', LinearSVC())
        ])

    def __init_naive_bayes_model(self) -> Pipeline:
        """Initalizes an untrained Mulitonomial Naive Bayes model.

        :return: Sklearn Pipeline with vectorization and prediction model.
        """
        return Pipeline([
            ('counter', CountVectorizer(stop_words=get_stop_words('english'))),
            ('tfidf', TfidfTransformer()),
            ('classifier', MultinomialNB())
        ])

    def __init_logistic_regression_model(self) -> Pipeline:
        """Initalizes an untrained Logistic Regression model.

        :return: Sklearn Pipeline with vectorization and prediction model.
        """
        return Pipeline([
            ('counter', CountVectorizer(stop_words=get_stop_words('english'))),
            ('tfidf', TfidfTransformer()),
            ('classifier', SGDClassifier(loss='log'))
        ])

    def __init_model(self, type: ModelType) -> Pipeline:
        """Intalizes a model of a given type.

        :param type: Type of model to initialize.
        :return: Sklearn pipeline of a given type.
        """
        if type == ModelType.SVM:
            return self.__init_svm_model()
        return self.__init_naive_bayes_model()

    def __create_metadata(self, model: Pipeline, type: ModelType,
                          training_data: DataList, test_data: DataList) -> Classifier:
        """Creates a metadata object for a trained model.

        :return: Classifier
        """
        classifier = Classifier(
            type = type.value,
            training_samples = len(training_data.labels),
            test_samples = len(test_data.labels),
            accuracy = self.__check_model_accuracy(model, test_data),
            model_hash = self.__calc_model_hash(type, training_data))
        self.__log.info(f'Trained model: {classifier}')
        return classifier

    def __check_model_accuracy(self, model: Pipeline, test_data: DataList) -> float:
        """Checks the prediction accuracy of a trained model.

        :param model: Trained model pipeline.
        :param test_data: Test data set as a DataList.
        :return: Accuracy score between 0.0 and 1.0
        """
        predictions = model.predict(test_data.texts)
        return f1_score(test_data.labels, predictions, average='micro')

    def __get_and_split_data(self) -> Tuple[DataList, DataList]:
        """Retrieves training data and splits between training and test data.

        :return: DataList with training data.
        :return: DataList with test data.
        """
        samples = self.__sample_repo.get_all()
        test_list = {s.id: s for s in samples[::5]}
        training_list = [s for s in samples if s.id not in test_list]
        test_data = self.__samples_to_datalist(test_list.values())
        training_data = self.__samples_to_datalist(training_list)
        return training_data, test_data

    def __samples_to_datalist(self, training_data: Iterable[TrainingData]) -> DataList:
        """Transformes a list of TrainingData into
        a DataList of texts and labels.

        :param training_data: TrainingData list.
        :return: DataList
        """
        texts = [format_text(td.text) for td in training_data]
        labels = [td.label for td in training_data]
        return DataList(texts=texts, labels=labels)

    def __calc_model_hash(self, type, training_data) -> str:
        """Calculates the sha1 hash of the data used to train the model.

        :param type: ModelType.
        :param training_data: DataList used for model training.
        :return: Hexdigest of the models training data
        """
        texts = ''.join([text for text in training_data.texts])
        labels = ''.join([label for label in training_data.labels])
        model_str = type.value + texts + labels
        return sha1((model_str).encode('utf-8')).hexdigest()


# Regex for identifiying URLs.
_URL_PATTERN = re.compile(r'(https?|ftp):\/\/[\.[a-zA-Z0-9\/\-]+')


def format_text(original: str) -> str:
    """Strips an original string of URLs, double, leading and trailing spaces.

    :param original: String to format.
    :return: Formated string.
    """
    return _URL_PATTERN.sub('', original).replace('  ', ' ').strip().lower()


def dummy_pipeline() -> Pipeline:
    """Creates an untrained placeholder pipeline"""
    return Pipeline([
        ('counter', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])
