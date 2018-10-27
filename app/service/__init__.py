# Internal modules
from app.config import TRAIN_MODEL
from app.models import ModelType
from .training_service import TrainingService
from .classification_service import ClassifcationService
from app.repository import TrainingDataRepo
from app.repository import ModelRepo


def __setup_classification_svc() -> ClassifcationService:
    training_svc = TrainingService(TrainingDataRepo())
    if not TRAIN_MODEL:
        return ClassifcationService(None)
    model_repo = __setup_model_repo()
    return ClassifcationService(model_repo)


def __setup_model_repo() -> ModelRepo:
    training_svc = TrainingService(TrainingDataRepo())
    svm_model, svm_classfier = training_svc.train_model(ModelType.SVM)
    nb_model, nb_classfier = training_svc.train_model(ModelType.NAIVE_BAYES)
    model_repo = ModelRepo(svm_model, nb_model)
    model_repo.save_classifier(svm_classfier)
    model_repo.save_classifier(nb_classfier)
    return model_repo


classification_svc: ClassifcationService = __setup_classification_svc()
