from flask import Flask, request, jsonify, Response, render_template
from sklearn.externals import joblib
from utils.prepv1 import FeatureProcessor
import traceback
import pandas as pd
import numpy as np
import sys
import json
import random
import time
from datetime import datetime

# Your API definition
app = Flask(__name__)
preprocessor = joblib.load('preprocessor_v1.0_pkl.pkl')
print('Model preprocessor loaded')
clf = joblib.load("XGB_SMOTE_v1.0_pkl.pkl")
print('Model classifer loaded')
model_columns = joblib.load("X_columns_v1.0_pkl.pkl")
print('Model columns loaded')

fraud_num = 0
all_num = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if clf:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            preprocessed_query = preprocessor.transform(query)
            preprocessed_query = preprocessed_query.reindex(columns=model_columns, fill_value=0)
            prediction = list(clf.predict(preprocessed_query))
            fraud_probs = list(clf.predict_proba(preprocessed_query)[:, 1])

            global fraud_num
            global all_num
            fraud_num += np.sum(prediction)
            all_num += len(prediction)

            return jsonify({'isFraud': str(prediction),
                            'fraud probability': str(fraud_probs)})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return('No model here to use')


@app.route('/chart-data')
def chart_data():
    def generate_data():
        while True:
            global fraud_num
            global all_num
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'valueFraud': str(fraud_num), 'valueAll': str(all_num)})
            fraud_num = 0
            all_num = 0
            yield f"data:{json_data}\n\n"
            time.sleep(5)

    return Response(generate_data(), mimetype='text/event-stream')


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])  # This is for a command-line input
    except:
        port = 12345  # If you don't provide any port the port will be set to 12345

    app.run(port=port, debug=True, threaded=True)
