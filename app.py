from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import numpy as np
from xgboost import DMatrix
model = joblib.load(os.path.join(os.getcwd(), "xg_model_modified.pkl"))

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def generate_graph():
    body = request.get_json() 
    time_arr = np.arange(0, 0.006, 0.00003)
    data_points = []
    print('hi')

    for i in time_arr:
        data_from_user = [[body["A"], body["B"], body["n"], body["C"], body["m"], body["velocity"], body["density"], body["impactor_mass"], body["length"], body["width"], body["thickness"]]]
        time = round(i, 5)
        data_from_user[0].insert(0, time)
        prdct = model.predict(data_from_user)
        disp = float(prdct[0])
        time_mod = round(time*1000, 2)
        disp_mod = round(disp*1000, 2)
        single_point = {
            "x": time_mod,
            "y": disp_mod
        }
        data_points.append(single_point)
    return jsonify(data_points), 200
if __name__ == '__main__':
    app.run(debug=False)