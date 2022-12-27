from flask import Flask, render_template
from flask_cors import cross_origin


app = Flask(__name__,
template_folder="templates",
static_folder="static")


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("home.html")

@app.route('/batch_prediction', methods=['POST', 'GET'])
def run_batch_prediction():
    return render_template("output.html")

@app.route('/custom_batch_prediction', methods=['POST', 'GET'])
def run_custom_batch_prediction():
    return render_template("output.html")