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
    --------------------------------------------------------------------------------------------------------------------------------
   CURRENT named methods are for the directory or objects which have been created when pipeline is started to produce new model.
   LATEST named methods are for the directory or object which have been created when pipeline was previously ran to produce model. 
   ---------------------------------------------------------------------------------------------------------------------------------
    input:
     - `model_registry`: directory containing all sub directories which contain the models trained and their transformers as well as encoder till now in  artifacts of model training component
     - `model_dir_name`: directory name containing models which is in (model_registry -> subdir -> model)
     - `transformer_dir_name`: directory name containing models which is in (model_registry -> subdir -> transformer_dir_name)
     - `target_encoder_dir_name`: directory name containing models which is in (model_registry -> subdir -> target_encoder_dir_name)
    --------------------------------------------------------------------------------------------------------------------------------
    return: `None`
    """ 

    def __init__(self,model_registry:str = "saved_models", transformer_dir_name="transformer", target_encoder_dir_name =        "target_encoder", model_dir_name = "model"):
        try:
            self.model_registry = model_registry
            os.makedirs(self.model_registry, exist_ok=True)

            self.transformer_dir_name  = transformer_dir_name

            self.target_encoder_dir_name = target_encoder_dir_name

            self.model_dir_name = model_dir_name
        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_dir_path(self)->Optional[str]:
        """
        Returns latest model directory path if their any
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
        return: `None` or `latest_dir_path`
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
    
    def get_latest_model_path(self):
        """
        Returns latest model path from the latest model subdir from model_registry
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
         return: `latest_model_path`
        """
        try:
            latest_dir_path = self.get_latest_dir_path()

            # If no model in the path
            if latest_dir_path is None:
                logging.log(f"Model is not available!")
                raise Exception(f"Model is not available!")

            latest_model_path = os.path.join(latest_dir_path, self.model_dir_name, MODEL_FILE_NAME)

            return latest_model_path

        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_transformer_path(self):
        """
        Returns latest transformer path from the latest transformer subdir from model_registry
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
         return: `latest_transformer_path`
        """
        try:
            latest_dir_path = self.get_latest_dir_path()

            # If no transformer in the path
            if latest_dir_path is None:
                logging.log(f"Transformer is not available!")
                raise Exception(f"Transformer is not available!")

            latest_transformer_path = os.path.join(latest_dir_path, self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME)

            return latest_transformer_path

        except Exception as e:
            raise SensorException(e, sys)
    
    def get_latest_target_encoder_path(self):
        """
        Returns latest target encoder path from the latest target encoder subdir from model_registry
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
         return: `latest_target_encoder_path`
        """
        try:
            latest_dir_path = self.get_latest_dir_path()

            # If no target encoder in the path
            if latest_dir_path is None:
                logging.log(f"Target encoder is not available!")
                raise Exception(f"Target encoder is not available!")

            latest_target_encoder_path = os.path.join(latest_dir_path, self.target_encoder_dir_name, TRANSFORMER_OBJECT_FILE_NAME)

            return latest_target_encoder_path

        except Exception as e:
            raise SensorException(e, sys)

    ##################################################

    def get_current_dir_path(self)->Optional[str]:
        """
        Returns current model directory path if their any
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
        return: `None` or `current_dir_path`
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
            current_dir_name = max(dir_names)

            # Get absolute path to our latest subdir
            current_dir_path = os.path.join(self.model_registry, f"{current_dir_name + 1}")

            return current_dir_path

        except Exception as e:
            raise SensorException(e, sys) 
    
    def get_current_model_path(self):
        """
        Returns current model path from the current model subdir from model_registry
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
         return: `current_model_path`
        """
        try:
            current_dir_path = self.get_current_dir_path()

            # If no model in the path
            if current_dir_path is None:
                logging.log(f"Model is not available!")
                raise Exception(f"Model is not available!")

            current_model_path = os.path.join(current_dir_path, self.model_dir_name, MODEL_FILE_NAME)

            return current_model_path

        except Exception as e:
            raise SensorException(e, sys)

    def get_current_transformer_path(self):
        """
        Returns current transformer path from the current transformer subdir from model_registry
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
         return: `current_transformer_path`
        """
        try:
            current_dir_path = self.get_current_dir_path()

            # If no transformer in the path
            if current_dir_path is None:
                logging.log(f"Transformer is not available!")
                raise Exception(f"Transformer is not available!")

            current_transformer_path = os.path.join(current_dir_path, self.transformer_dir_name, TRANSFORMER_OBJECT_FILE_NAME)

            return current_transformer_path

        except Exception as e:
            raise SensorException(e, sys)
    
    def get_current_target_encoder_path(self):
        """
        Returns current target encoder path from the current target encoder subdir from model_registry
        ---------------------------------------------------------
        input:
         - `None`
        ---------------------------------------------------------
         return: `current_target_encoder_path`
        """
        try:
            current_dir_path = self.get_current_dir_path()

            # If no target encoder in the path
            if current_dir_path is None:
                logging.log(f"Target encoder is not available!")
                raise Exception(f"Target encoder is not available!")

            current_target_encoder_path = os.path.join(current_dir_path, self.target_encoder_dir_name, TRANSFORMER_OBJECT_FILE_NAME)

            return current_target_encoder_path

        except Exception as e:
            raise SensorException(e, sys)