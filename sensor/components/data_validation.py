"Data Validation Component"


import os
import sys
import numpy as np
import pandas as pd
from typing import Optional
from scipy.stats import ks_2samp
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.config import TARGET_COLUMN
from sensor.logger import logging
from sensor.exception import SensorException
from sensor import utils


class DataValidation:
    """
    Data Validation Component
    ---------------------------------------------------------
    input:
     - data_validation_config: Data Validation Configuration
     - data_ingestion_artifact: Data Ingestion Artifact
    ---------------------------------------------------------
    return: Data Validation Artifact
    """

    def __init__(self, data_validation_config: config_entity.DataValidationConfig, data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info("Collecting Data Ingestion Configuration")
            
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact

            # Initializing dictionary for storing validation error
            self.validation_error = dict()

        except Exception as e:
            raise SensorException(e, sys)
        
    def drop_missing_values_columns(self, df: pd.DataFrame, report_key: str)-> Optional[pd.DataFrame]:
        """
        Drops the columns from DataFrame which have null value percent more than threshold
        ------------------------------------------------------------
        input:
         - df: DataFrame from which to drop the columns
         - report_key_: Name of the key with which to save report in `self.validation_error` attribute
         -----------------------------------------------------------
         return: `None` if no columns left else `pd.DataFrame`
        """

        try:
            # Defining threshold for missing values
            logging.info(f"Initializing threshold as {self.data_validation_config.missing_value_threshold}")
            threshold = self.data_validation_config.missing_value_threshold

            # Calculate the percentage of null values in columns
            logging.info(f"Calculating the percentage of null values in columns")
            null_report = df.isna().sum() / df.shape[0]

            # Select columns which have null value percentage more than threshold
            drop_column_names = null_report[null_report > threshold].index
            logging.info(f"Columns which have null value percentage more than threshold: {drop_column_names}")

            # Add report about columns to drop
            logging.info(f"Adding report about columns to drop to validation_error attribute")
            self.validation_error[report_key] = list(drop_column_names)

            # Dropping the columns whose null value percent exceeds the threshold
            logging.info(f"Dropping the columns whose null value percent exceeds the threshold")
            df.drop(list(drop_column_names), axis=1, inplace =True)

            # Return None if no column left, else Return DataFrame
            if len(df.columns) == 0:
                return None
            return df

        except Exception as e:
            raise SensorException(e, sys)

    def is_required_columns_exist(self,base_df: pd.DataFrame, current_df: pd.DataFrame, report_key: str)-> bool:
        """
        Drops the columns from DataFrame which have null value percent more than threshold
        ------------------------------------------------------------
        input:
         - base_df: DataFrame from which we are validating(base info)
         - current_df: DataFrame which we are validating
         - report_key_: Name of the key with which to save report in `self.validation_error` attribute
         -----------------------------------------------------------
         return: `True` if required columns exist else `False`
        """

        try:
            # Initializing columns of base and current data frame
            base_columns = base_df.columns
            current_columns = current_df.columns

            # Initializing missing columns to store missing column names
            missing_columns = []

            # Checking for the columns which are in base data frame but not in current data frame
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)
            
            # Return True if missing columns, else Return False and add to report
            if len(missing_columns) > 0:
                self.validation_error[report_key] = missing_columns
                return False
            return True

        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self):...


    def initiate_data_validation(self):...