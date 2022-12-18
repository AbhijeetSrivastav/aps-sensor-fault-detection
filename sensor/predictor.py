"Predictor for sensor package"


import sys
import os
from glob import glob 
from typing import Optional
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME, TARGET_ENCODER_FILE_OBJECT_NAME


class ModelResolver:
    """
    Model Resolver 
    ---------------------------------------------------------
    input:
     - `model_registry`: directory containing all sub directories of the models trained till now in  artifacts of model training component
     - `model_dir_name`: directory containing latest model within `model_registry`
     - `transformer_dir_name`: directory containing artifact of data transformation component
     - `target_encoder_dir_name`: directory containing the target encoder object which is artifact of data transformation component
    ---------------------------------------------------------
    return: `None`
    """ 

    def __init__(self,model_registry:str = "saved_models", transformer_dir_name="transformer", target_encoder_dir_name =        "target_encoder", model_dir_name = "model"):
        try:
            self.model_registry = model_registry
            os.makedirs(self.model_registry, exist_ok=True)

            self.transformer_dir_name  = transformer_dir_name

            self.target_encoder_dir_name = target_encoder_dir_name

            self.model_directory_name = model_dir_name
        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_dir_path(self)->Optional[str]:
        """
        Returns latest model directory path if their any
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
         return: `None` or `latest_dir_name`
        """
        try:
            # Creating list of all the sub directories in the model_registry folder of model training artifact
            dir_names = os.listdir(self.model_registry)

            # If no sub directory that means no saved model object
            if len(dir_names) == 0:
                return None
            

            # Convert str name of subdir to int for all subdirs
            dir_names = list(map(int, dir_names))


            # Get the latest one as we saved our subdirs as named by date time format
            latest_dir_name = max(dir_names)

            # Get absolute path to our latest subdir
            latest_dir_path = os.path.join(self.model_registry, f"{latest_dir_name}")

            return latest_dir_path

        except Exception as e:
            raise SensorException(e, sys) 

    