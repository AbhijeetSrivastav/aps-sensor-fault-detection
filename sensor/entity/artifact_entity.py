"Contain all the artifacts of the components and pipelines"


from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """
    Artifact for Data Ingestion component
    ---------------------------------------
    return:
    - `feature_store_file_path`: path of feature store of data ingestion component
    - `train_file_path`: path of train file created by Data Ingestion component
    - `test_file_path`: path of test file created by Data Ingestion component
    """
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifact:
    """
    Artifact for Data Validation component
    ---------------------------------------
    return:
    - `report_file_path`: path of the validation report
    """
    report_file_path:str


@dataclass
class DataTransformationArtifact:
    """
    Artifact for Data Transformation component
    ---------------------------------------
    return:
    - `transformer_object_path`: path of the transformer object
    - `transformed_train_path`: path of the transformed train dataset array
    - `transformed_test_path`: path of the transformed test dataset array
    - `target_encoder_path`: path of the target encoder object
    """
    transformer_object_path: str
    transformed_train_path: str
    transformed_test_path: str
    target_encoder_path: str


@dataclass
class ModelTrainerArtifact:
    """
    Artifact for Model Training component
    ---------------------------------------
    return:
    - `model_path`: path of the model object
    - `f1_train_score`: f1 score of train set
    - `f1_test_score`: f1 score of test set
    """
    model_path: str
    f1_train_score: float
    f1_test_score: float


@dataclass
class ModelEvaluationArtifact:...


@dataclass
class ModelPusherArtifact:...
