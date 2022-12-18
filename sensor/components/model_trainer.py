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

    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        """
        Initiates Model Trainer Component
        ------------------------------------------------------------
        input: `None`
         -----------------------------------------------------------
        return: Model Trainer Artifact
        """

        try:     
            # Load train 
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)

            # Load test array
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            # Split train array in input and target feature array
            x_train, y_train = train_arr[:, :, -1], train_arr[:,-1]

            # Split test array in input and target feature array
            x_test, y_test = test_arr[:, :, -1], test_arr[:, -1]

            # Create model object and fit the model
            model = self.train_model(x=x_train, y=y_train)

            # Predict the value of target using model for training array
            y_hat_train = model.predict(x_train)

            # Calculate f1 score for training array
            f1_train_score = f1_score(y_true=y_train, y_pred=y_hat_train)

            # Predict the value of target using model for test array
            y_hat_test = model.predict(x_test)

            # Calculate f1 score for test array
            f1_test_score = model.predict(y_true=y_test, y_pred=y_hat_test)

            # Check for underfitting
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is Underfitting ! Expected Score:: {self.model_trainer_config.expected_score} Achieved Score:: {f1_test_score}")

            # Check for overfitting
            diff = abs(f1_train_score, f1_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Model is Overfitting! Expected Threshold:: {self.model_trainer_config.overfitting_threshold} Diff of train and test score:: {diff}")

            # Save the trained model object
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # Prepare the artifact
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)

            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys)