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
     - `model_registry`: directory containing model t
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

