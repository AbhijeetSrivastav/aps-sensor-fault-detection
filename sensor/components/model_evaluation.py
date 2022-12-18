"Model Evaluation Component"


import sys
import os
import pandas as pd
from sklearn.metrics import f1_score
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor. config import TARGET_COLUMN
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils


class ModelEvaluation:
    """
        Model Evaluation Component
        ---------------------------------------------------------
        input:
         - `model_evaluation_config`: Model Evaluation Configuration
         - `data_ingestion_artifact`: Data Ingestion Artifact
         - `data_transformation_artifact`: Data Transformation Artifact
         - `model_trainer_artifact`: Model Trainer Artifact
        ---------------------------------------------------------
         return: Model Evaluation Artifact
        """

    def __init__(self, model_evaluation_config: config_entity.ModelEvaluationConfig, data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
    data_transformation_artifact: artifact_entity.DataTransformationArtifact, model_trainer_artifact: artifact_entity.ModelTrainerArtifact):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)
            

