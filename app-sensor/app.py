from flask import Flask, render_template, request
from flask_cors import cross_origin

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
            start_batch_prediction(input_file_path='aps_failure_training_set1.csv', api=True)
            return render_template("output.html")
        except Exception as e:
            raise e