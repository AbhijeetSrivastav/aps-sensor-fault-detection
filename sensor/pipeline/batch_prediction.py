"Batch Prediction"


import sys
import os
from datetime import datetime
import pandas as pd
import numpy as np
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import load_object
from sensor.predictor import ModelResolver


PREDICTION_DIR = "prediction"


def start_batch_prediction(input_file_path):
    """
    Predicts output label for batch of data points
    -----------------------------------------------------
    input:
    - `input_file_path`: file which contains all the data 
                    points in form of rows and columns
    ------------------------------------------------------
    return: `prediction_file_path`
    """
    try:
        # Making prediction directory
        logging.info(f"Creating prediction directory if not exist")
        os.makedirs(PREDICTION_DIR, exist_ok=True)
    
        # Loading model resolver
        logging.info(f"Loading model resolver class")
        model_resolver = ModelResolver(model_registry="saved_model")

        # Loading the dataset on whose values we want to make predictions (in batch)
        logging.info(f"Loading dataset on which to predict")
        df = pd.read_csv(input_file_path)

        # Replacing na values with Nan
        df.replace({"na": np.NAN}, inplace=True)

        # Load latest transformer object
        logging.info(f"Loading latest transformer object")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())

        # Extract input features from transformer object
        logging.info(f"Extracting input feature from transformer object")
        input_feature_names =  list(transformer.feature_names_in_)
        
        # Convert input feature dataframe into array
        logging.info(f"Converting input feature dataframe into array")
        input_arr = transformer.transform(df[input_feature_names])

        # Load latest model object
        logging.info(f"Loading latest model object")
        model = load_object(file_path=model_resolver.get_latest_model_path())

        # Predict using model
        logging.info(f"Predicting output label using model")
        prediction = model.predict(input_arr)

        # Load latest target encoder object
        logging.info(f"Loading latest target encoder object")
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())

        # Inverse transform target feature
        logging.info(f"Inverse transforming encoded target features") 
        cat_prediction = target_encoder.inverse_transform(prediction)

        # Dataframe having prediction and category
        df["prediction"]=prediction
        df["cat_pred"]=cat_prediction

        # Save prediction file
        logging.info(f"Saving prediction file containing prediction for input file")
        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)

        df.to_csv(prediction_file_path,index=False,header=True)

        return prediction_file_path
        
    except Exception as e:
        raise SensorException(e, sys)