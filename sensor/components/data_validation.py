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
     - `data_validation_config`: Data Validation Configuration
     - `data_ingestion_artifact`: Data Ingestion Artifact
    ---------------------------------------------------------
    return: Data Validation Artifact
    """

    def __init__(self, data_validation_config: config_entity.DataValidationConfig, data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info("Collecting Data Validation Configuration")
            self.data_validation_config = data_validation_config
            
            logging.info("Collecting Data Ingestion Artifact")
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
         - `df`: DataFrame from which to drop the columns
         - `report_key_`: Name of the key with which to save report in self.validation_error attribute
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
         - `base_df`: DataFrame from which we are validating(base info)
         - `current_df`: DataFrame which we are validating
         - `report_key_`: Name of the key with which to save report in self.validation_error attribute
         -----------------------------------------------------------
         return: `True` if required columns exist else `False`
        """

        try:
            # Initializing columns of base and current data frame
            logging.info(f"Initializing columns of base and current data frame")
            base_columns = base_df.columns
            current_columns = current_df.columns

            # Initializing missing columns to store missing column names
            missing_columns = []

            # Checking for the columns which are in base data frame but not in current data frame
            logging.info(f"Checking for the columns which are in base data frame but not in current data frame")
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)
            
            # Return True if missing columns, else Return False and add to report
            if len(missing_columns) > 0:
                logging.info(f"No missing column found")
                self.validation_error[report_key] = missing_columns
                return False
            
            logging.info(f"Missing column found")
            return True

        except Exception as e:
            raise SensorException(e, sys)

    def data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key: str):
        """
        Calculates Data Drift in base and current DataFrame
        
        - Null hypothesis is that both column data are drawn from same distribution.
        ------------------------------------------------------------ 
        input:
         - `base_df`: DataFrame from which we are validating(base info)
         - `current_df`: DataFrame which we are validating
         - `report_key_`: Name of the key with which to save report in self.validation_error attribute
         -----------------------------------------------------------
         return: `None`
        """

        try:
            # Initializing data drift dict to store drift stats
            logging.info(f"Initializing data drift dictionary")
            drift_report = dict()

            # Initializing columns of base and current data frame
            logging.info(f"Initializing columns of base and current data frame")
            base_columns = base_df.columns
            current_columns = current_df.columns

            # Collecting for each column in base dataframe
            for base_column in base_columns:
                # ---NULL HYPOTHESIS---
                # Creating base_data and current_data DataFrame only for all the columns which are common in base and current dataFrame
                logging.info(f"Creating base and current data")
                base_data, current_data = base_df[base_column], current_df[base_column]

                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")

                # Checking distribution 
                logging.info(f"Calculating stats for distribution analysis")
                same_distribution = ks_2samp(base_data, current_data)

                # Updating drift report based on same_distribution
                logging.info(f"Creating drift report for distribution")
                if same_distribution.pvalue > 0.05:
                    # ---Accepting NULL HYPOTHESIS---
                    logging.info(f"Accepting Null Hypothesis")
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    # ---Rejecting NULL HYPOTHESIS---
                    logging.info(f"Rejecting Null Hypothesis")
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "same_distribution": False
                    }

            # Adding report about distribution
            logging.info(f"Adding report about drift in validation error")
            self.validation_error[report_key] = drift_report

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
