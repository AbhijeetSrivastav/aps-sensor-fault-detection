"Model Evaluation Component"


import sys
import pandas as pd
from sklearn.metrics import f1_score
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor. config import TARGET_COLUMN
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.predictor import ModelResolver
from sensor import utils



class ModelEvaluation:
    """
    Model Evaluation Component
    ---------------------------------------------------------
    input:
     - `model_evaluation_config`: Model Evaluation Configuration
     - `data_ingestion_artifact`: Data Ingestion Artifact
     - `data_transformation_artifact`: Data Transformation Artifact
     - `model_trainer_artifact`: Model Trainer Artifact
    ---------------------------------------------------------
    return: Model Evaluation Artifact
    """

    def __init__(self, model_evaluation_config: config_entity.ModelEvaluationConfig, data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
    data_transformation_artifact: artifact_entity.DataTransformationArtifact, model_trainer_artifact: artifact_entity.ModelTrainerArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config

            self.data_ingestion_artifact = data_ingestion_artifact

            self.data_transformation_artifact = data_transformation_artifact

            self.model_trainer_artifact = model_trainer_artifact
            
            # Initiating model resolver
            logging.info(f"Initiating Model Resolver")
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise SensorException(e, sys)
            
    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        """
        Initiates Model Evaluation Component
        ------------------------------------------------------------
        input: 
         - `None`
        -----------------------------------------------------------
        return: Model Evaluation Artifact
        """

        try:
            "FOR LATEST MODEL FROM PREVIOUSLY SAVED"
            logging.info(f"Fetching path of latest model, transformer, target encoder")
            # latest model directory path 
            latest_dir_path = self.model_resolver.get_latest_dir_path()


            # If their is no model accept the current trained model and prepare artifact
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)

                return model_eval_artifact
            

            #---If their are previously saved model then we will compare---
            
            # Fetching path of latest model,transformer and target encoder
            latest_transformer_path = self.model_resolver.get_latest_transformer_path()

            latest_model_path = self.model_resolver.get_latest_model_path()

            latest_target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            
            # Loading latest model, transformer and target encoder object
            logging.info(f"Loading latest model, transformer, target encoder objects")
            latest_transformer = utils.load_object(file_path=latest_transformer_path)

            latest_model = utils.load_object(file_path=latest_model_path)

            latest_target_encoder = utils.load_object(file_path=latest_target_encoder_path)

         
            "FOR CURRENT MODEL THAT WE TRAINED IN THIS RUN OF PIPELINE AND SAVED"
            logging.info(f"Fetching path of current model, transformer, target encoder")
            # Fetching path of current model,transformer and target encoder
            current_transformer_path = self.data_transformation_artifact.transformer_object_path

            current_model_path = self.model_trainer_artifact.model_path

            current_target_encoder_path = self.data_transformation_artifact.target_encoder_path


            # Loading current model, transformer and target encoder object
            logging.info(f"Loading current model, transformer, target encoder objects")
            current_transformer = utils.load_object(file_path=current_transformer_path)

            current_model = utils.load_object(file_path=current_model_path)

            current_target_encoder = utils.load_object(file_path=current_target_encoder_path)


            # Loading test dataframe
            logging.info(f"Loading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # Splitting test dataframe in target and input feature
            logging.info(f"Splitting test dataframe in target and input feature")
            target_df = test_df[TARGET_COLUMN]

            y_true = latest_target_encoder.transform(target_df)

            # Accuracy using latest model
            logging.info(f"Calculating accuracy for latest model")
            input_feature_name = list(latest_transformer.feature_names_in_)

            input_arr = latest_transformer.transform(test_df[input_feature_name])

            y_pred = latest_model.predict(input_arr)

            latest_model_score = f1_score(y_true=y_true, y_pred=y_pred)


            # Accuracy using the current model
            logging.info(f"Calculating accuracy for current model")
            input_feature_name = list(current_transformer.feature_names_in_)

            input_arr = current_transformer.transform(test_df[input_feature_name])

            y_pred = current_model.predict(input_arr)

            y_true = latest_target_encoder.transform(target_df)

            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)    

            # Comparing models
            logging.info(f"Comparing accuracy of latest and current model")
            if current_model_score <= latest_model_score:
                raise Exception("Current trained model is not better than previous model")
            

            logging.info(f"Latest model accuracy:: {latest_model_score}, Current model accuracy:: {current_model_score}")

            # Calculating accuracy score diff
            diff = current_model_score - latest_model_score

            # Preparing artifact
            logging.info(f"Preparing Model Evaluation artifacts")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=diff)
        
            return model_eval_artifact

        except Exception as e:
            raise SensorException(e, sys)