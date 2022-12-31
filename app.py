from flask import Flask, render_template, request, send_file
from flask_cors import cross_origin

import pandas as pd

from sensor.pipeline.batch_prediction import start_batch_prediction
from sensor.predictor import ModelResolver

app = Flask(__name__,
template_folder="templates",
static_folder="static")


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("home.html")

@app.route('/batch_prediction', methods=['POST', 'GET'])
def run_batch_prediction():
    if request.method == "POST":
        try:
            run_batch_prediction.prediction_file_path = start_batch_prediction(input_file_path='aps_failure_training_set1.csv')

            # prediction_df = pd.concat((chunk for chunk in pd.read_csv(prediction_file_path,chunksize=100)))

            prediction_df = pd.read_csv(run_batch_prediction.prediction_file_path).head(1000)

            return render_template("output.html", tables=[prediction_df.to_html(classes="dataframe", header=True)], titles=prediction_df.columns.values)

        except Exception as e:
            raise e


@app.route('/download_batch_prediction') 
def download_batch_prediction():
    return send_file(run_batch_prediction.prediction_file_path,
        mimetype='text/csv',
        download_name='prediction.csv',
        as_attachment=True
    )