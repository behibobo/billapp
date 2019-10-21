import helper
import pandas as pd
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      print(request.files['file'])
      f = request.files['file']
      data_xls = pd.read_excel(f, sheet_name="Export Worksheet",
      converters={'SHOMARE_PARDAKHT':str, 'SHOMARE_BADANE':str,'SHOMARE_GABZ':str,'SHOMARE_ESHTERAK':str,'MABLAGHE_GABELE_PARDAKHT':str,'MOHLATE_PARDAKHT':str,'NAME':str,})
      for index, row in data_xls.iterrows():
        helper.add_item(row)
         
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''

@app.route('/bills', methods=['GET'])
@cross_origin()
def get_items():
    bills = helper.get_all_bills()
    if bills is None:
        response = Response("{'error': 'Item not added - '}" , status=400, mimetype='application/json')
        return response

    response = Response(json.dumps(bills), mimetype='application/json')

    return response

@app.route('/bill/get', methods=['POST'])
@cross_origin()
def get_bill():

    req_data = request.get_json()
    print(req_data)
    bill_serial = req_data['bill_serial']
    payment_serial = req_data['payment_serial']

    # Add item to the list
    bill = helper.get_bill(bill_serial, payment_serial)
    print(bill)
    # Return error if item not added
    if bill is None:
        response = Response("{'error': 'Item not added - '}" , status=400, mimetype='application/json')
        return response

    # Return response
    data = {
        "customer_serial": bill[1],
        "bill_serial": bill[2],
        "payment_serial": bill[3],
        "amount": bill[4],
        "customer": bill[5],
        "valid_to": bill[6],
        "chasis_serial": bill[7],
    }
    response = Response(json.dumps(data), mimetype='application/json')

    return response


if __name__ == "__main__":
    app.run()
