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

            logging.info(f"Creating transformation object")
            pipeline = Pipeline(steps=[
                ("Imputer", simple_imputer),
                ("RobustScaler", robust_scaler)
            ])

            return pipeline

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        """
        Initiates Data Transformation Component
        ------------------------------------------------------------
        input: `None`
         -----------------------------------------------------------
        return: Data Transformation Artifact
        """

        try:
            # Reading train file
            logging.info(f"Reading train file")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)

            # Reading test file
            logging.info(f"Reading test file")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # Selecting input feature from train dataframe
            logging.info(f"Selecting input feature from train dataframe")
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)

            # Selecting input feature from test dataframe
            logging.info(f"Selecting input feature from test dataframe")
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)

            # Selecting target feature from train dataframe
            logging.info(f"Selecting target feature from train dataframe")
            target_feature_train_df = train_df[TARGET_COLUMN]

            # Selecting target feature from test dataframe
            logging.info(f"Selecting target feature from test dataframe")
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Creating and fitting Label encoder object
            logging.info(f"Creating and fitting Label Encoder object")
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            # Encoding target feature of train dataframe
            logging.info(f"Transforming target feature of train dataframe using label encoder object")
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)

            # Encoding target feature of test dataframe
            logging.info(f"Transforming target feature of test dataframe using label encoder object")
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            # Fetching and fitting transformation pipeline
            logging.info(f"Fetching transformation object, creating & fitting transformation pipeline")
            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            # Transforming input feature of train dataframe
            logging.info(f"Transforming input feature of train dataframe using transformation pipeline")
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)

            # Transforming input feature of test dataframe
            logging.info(f"Transforming input feature of test dataframe using transformation pipeline")
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            # Creating SMOTETomek object for resampling
            logging.info(f"Creating SMOTETomek object for resampling")
            smt = SMOTETomek(random_state=42)

            # Resampling input and target feature of train array
            logging.info(f"Resampling input and target feature array of train dataframe using SMOTETomek object having shape: Input:: {input_feature_train_arr.shape} Target:: {target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"Shape after resampling: Input:: {input_feature_train_arr.shape} Target:: {target_feature_train_arr.shape}")

            # Resampling input and target feature of test array
            logging.info(f"Resampling input and target feature array of test dataframe using SMOTETomek object having shape: Input:: {input_feature_test_arr.shape} Target:: {target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"Shape after resampling: Input:: {input_feature_test_arr.shape} Target:: {target_feature_test_arr.shape}")
        
            # Preparing array version of train dataframe
            logging.info(f"Preparing array version of train dataframe using input and target array after encoding, transformation & resampling")
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]

            # Preparing array version of test dataframe
            logging.info(f"Preparing array version of test dataframe using input and target array after encoding, transformation & resampling")
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            # Saving train array as artifact
            logging.info(f"Saving train array as artifact")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)

            # Saving test array as artifact
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)

            # Saving transformer object
            logging.info(f"Saving transformer object")
            utils.save_object(file_path=self.data_transformation_config.transformer_object_path, obj=transformation_pipeline)

            # Saving label encoder object
            logging.info(f"Saving label encoder object")
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)

            # Preparing artifact 
            logging.info(f"Preparing Data Transformation artifacts")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transformer_object_path = self.data_transformation_config.transformer_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)