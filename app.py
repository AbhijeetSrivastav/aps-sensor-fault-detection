from flask import Flask, render_template, request, send_file, session, url_for, redirect
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

import os
import pandas as pd

from sensor.pipeline.batch_prediction import start_batch_prediction
from sensor.pipeline.training_pipeline import start_training_pipeline

app = Flask(__name__,
template_folder="templates",
static_folder="static")
UPLOAD_FOLDER = 'static\\files\\'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.secret_key ="xy"

@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("home.html")

@app.route('/batch_prediction', methods=['POST', 'GET'])
def run_batch_prediction():
    if request.method == "POST":
        try:
            run_batch_prediction.prediction_file_path = start_batch_prediction(input_file_path='aps_failure_training_set1.csv')

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

@app.route('/uploader', methods=['POST', 'GET']) 
def uploader():
    if request.method == "POST":
        # accessing uploaded file name
        uploaded_file = request.files['file']

        # extracting uploaded file name
        data_filename  = secure_filename(uploaded_file.filename)

        # flask upload file 
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], data_filename))
        print(os.path.join(app.config["UPLOAD_FOLDER"], data_filename))

        # storing uploaded file path in flask session
        session["uploaded_file_path"] = os.path.join(app.config["UPLOAD_FOLDER"], data_filename)


        return redirect(url_for("custom_batch_prediction"))

@app.route('/upload_form', methods=['POST', 'GET'])
def upload_form():
    return render_template("uploadForm.html")


@app.route('/custom_batch_prediction', methods=['POST', 'GET'])
def custom_batch_prediction():
    try:
        uploaded_file_path = session.get("uploaded_file_path", None)

        # Renaming uploaded file to fit it in prediction file format
        rename_as = "aps_failure_training_set.csv"
        try:
            os.rename(UPLOAD_FOLDER + os.path.basename(uploaded_file_path), UPLOAD_FOLDER + rename_as)
        except WindowsError:
            os.remove(os.path.join(UPLOAD_FOLDER,rename_as))
            os.rename(UPLOAD_FOLDER + os.path.basename(uploaded_file_path), UPLOAD_FOLDER + rename_as)
            
        renamed_uploaded_file_path = os.path.join(UPLOAD_FOLDER, rename_as)

        # Performing batch prediction for custom dataset
        custom_batch_prediction.prediction_file_path = start_batch_prediction(input_file_path=renamed_uploaded_file_path)

        custom_prediction_df = pd.read_csv(custom_batch_prediction.prediction_file_path).head(1000)

        return render_template("customOutput.html", tables=[custom_prediction_df.to_html(classes="dataframe", header=True)], titles=custom_prediction_df.columns.values)

    except Exception as e:
        raise e


@app.route('/download_custom_batch_prediction') 
def download_custom_batch_prediction():
    return send_file(custom_batch_prediction.prediction_file_path,
        mimetype='text/csv',
        download_name='prediction.csv',
        as_attachment=True
    )

@app.route('/retrain', methods=['POST', 'GET'])
def retrain():
    try:
        start_training_pipeline()
    except Exception as e:
        raise e