"Model Trainer Component"


import os
import sys
from typing import Optional
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.logger import logging
from sensor.exception import SensorException
from sensor import utils


class ModelTrainer:
    """
    Model Trainer Component
    ---------------------------------------------------------
    input:
     - `model_trainer_config`: Model Trainer Configuration
     - `data_transformation_artifact`: Data Transformation Artifact
    ---------------------------------------------------------
    return: Model Trainer Artifact
    """
    def __init__(self, model_trainer_config: config_entity.ModelTrainingConfig, data_transformation_artifact: artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config

            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def train_model(self, x: np.array, y: np.array)->XGBClassifier:
        """
        Creates a XGBClassifier which was selected during the experimentation
        ------------------------------------------------------------
        input:
         - `x`: input feature array
         - `y`: target feature array
        ------------------------------------------------------------
        return: `XGBClassifier`
        """
        try: 
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x, y)

            return xgb_clf

        except Exception as e:
            raise SensorException(e, sys)