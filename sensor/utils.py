"Utility function for sensor package"


import os
import sys
import yaml
import dill
import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """
    Collects a MongoDB database collection and returns a dataframe of it
    ---------------------------------------------------------------------
    input: 
    - database_name: Name of the database
    - collection_name: Name of the collection of the database
    ----------------------------------------------------------------------
    return: Pandas Dataframe of the collection of the database
    """

    try:
        # Reading data from database
        logging.info(f"Converting collection: {collection_name} from MongoDB: {database_name} into Data Frame")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))

        logging.info(f"DataFrame shape: {df.shape}")

        # Dropping the default id column if any
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df = df.drop("_id", axis=1)

        logging.info(f"DataFrame shape: {df.shape}")

        return df

    except Exception as e:
        raise SensorException(e, sys)