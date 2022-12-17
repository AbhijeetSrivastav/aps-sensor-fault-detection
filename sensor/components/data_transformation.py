"Data Transformation Component"

import os
import sys
from typing import Optional
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek
from sensor.entity import artifact_entity
from sensor.entity import config_entity
from sensor.config import TARGET_COLUMN
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils


class DataTransformation:
    """
    Data Transformation Component
    ---------------------------------------------------------
    input:
     - `data_transformation_config`: Data Transformation Configuration
     - `data_ingestion_artifact`: Data Ingestion Artifact
    ---------------------------------------------------------
    return: Data Transformation Artifact
    """

    def __init__(self, data_transformation_config: config_entity.DataTransformationConfig, data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config =  data_transformation_config

            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)

    
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        """
        Creates a pipeline based on experimentation done during EDA
        ------------------------------------------------------------
        input:
         - `None` 
        ------------------------------------------------------------
        return: `Pipeline`
        """
        
        try:
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)

            robust_scaler = RobustScaler()

            pipeline = Pipeline(steps=[
                ("Imputer", simple_imputer),
                ("RobustScaler", robust_scaler)
            ])

            return pipeline

        except Exception as e:
            raise SensorException(e, sys)