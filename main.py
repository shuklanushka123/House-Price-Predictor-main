import pandas as pd
import numpy as np
from flask import Flask , render_template, request
import pickle
import json

app = Flask(__name__)


__locations = None
__data_columns = None
ridge = pickle.load(open("RidgeModel.pickle", 'rb'))

f = open('columns.json')
__data_columns = json.loads(f.read())['data_columns']
__locations = __data_columns[3:]


def get_estimated_price(input_json):
    try:
        loc_index = __data_columns.index(input_json['Address'].lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = input_json['area']
    x[1] = input_json['Bedrooms']
    x[2] = input_json['Bathrooms']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(ridge.predict([x])[0],2)
    return result



@app.route('/')
def index():
    return render_template('index.html' ,locations = __locations )


@app.route('/predict', methods = ['POST'])
def predict():
    if request.method == 'POST':
        input_json = {
            "location": request.form['sLocation'],
            "area": request.form['Squareft'],
            "Bedrooms": request.form['uiBHK'],
            "Bathrooms": request.form['uiBathrooms']
        }
        result = get_estimated_price(input_json)


    return render_template('predict.html',result=result)

if __name__ == "__main__":
    app.run(debug=False)
