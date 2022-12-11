"Script to dumpy CSV dataset into MongoDB database"

import pymongo
import pandas as pd
import numpy as np
import json
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()


DATA_FILE_PATH = "./aps_failure_training_set1.csv"
DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"
MongoDB_Password = os.environ.get("MONGODB_KEY")
print(MongoDB_Password)


if __name__ == "__main__":

    # Connecting to the MongoDB client
    client = pymongo.MongoClient(f"mongodb+srv://abhijeet:{MongoDB_Password}@cluster0.bzvj4n2.mongodb.net/?retryWrites=true&w=majority")

    # Reading the CSV Dataset
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows: {df.shape[0]} Columns: {df.shape[1]}")

    # Dropping the default index of the data frame
    df.reset_index(drop=True, inplace=True)

    # Convert data frame to json 
    json_record = list(json.loads(df.T.to_json()).values())

    # Dump the json record to MongoDB database
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)