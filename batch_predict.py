"Main file batch prediction"


from sensor.pipeline.batch_prediction import start_batch_prediction
from sensor.logger import logging


FILE_FOR_BATCH_PREDICTION = "aps_failure_training_set1.csv"

if __name__=="__main__":
    try:
        logging.info(f"------------Initiating Batch Prediction------------")
        start_batch_prediction(input_file_path=FILE_FOR_BATCH_PREDICTION)
    except Exception as e:
        print(e)