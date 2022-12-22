"Mode Pusher Component"


import sys
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import load_object, save_object
from sensor.predictor import ModelResolver


class ModelPusher:
    """
    Model Pusher Component
    ---------------------------------------------------------
    input:
     - `model_pusher_config`: Model Pusher Configuration
     - `data_transformation_artifact`: Data Transformation Artifact
     - `model_trainer_artifact`: Model Trainer Artifact
    ---------------------------------------------------------
    return: Model Pusher Artifact
    """

    def __init__(self, model_pusher_config: config_entity.ModelPusherConfig, data_transformation_artifact: artifact_entity.DataTransformationArtifact, model_trainer_artifact: artifact_entity.ModelTrainerArtifact ):
        try:
            self.model_pusher_config=model_pusher_config
            
            self.data_transformation_artifact=data_transformation_artifact
            
            self.model_trainer_artifact=model_trainer_artifact
            
            # Initiating Model Resolver
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise SensorException(e, sys)
    
    def initiate_model_pusher(self)->artifact_entity.ModelPusherArtifact:
        """
        Initiates Model Pusher Component
        ------------------------------------------------------------
        input: `None`
        -----------------------------------------------------------
        return: Model Pusher Artifact
        """

        try:
            # Load transformer object
            logging.info(f"Loading transformer object")
            transformer = load_object(file_path=self.data_transformation_artifact.transformer_object_path)

            # Load Model object
            logging.info(f"Loading model object")
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            
            # Load target encoder object
            logging.info(f"Loading target encoder object")
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            # Save Model, transformer and encoder to model Pusher directory 
            logging.info(f"Saving model, transformer, target encoder object to model pusher directory")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)

            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)

            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)


            # Fetch path of latest model, transformer and encoder path
            logging.info(f"Fetching path of latest model, transformer, target encoder")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()

            model_path = self.model_resolver.get_latest_save_model_path()

            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            # Save Model, transformer and encoder to the saved model directory
            logging.info(f"Saving model, transformer, target encoder object to saved model directory")
            save_object(file_path=transformer_path, obj=transformer)

            save_object(file_path=model_path, obj=model)

            save_object(file_path=target_encoder_path, obj=target_encoder)

            # Prepare artifact
            logging.info(f"Preparing Pusher artifacts")
            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
             saved_model_dir=self.model_pusher_config.saved_model_dir)
           
            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys)