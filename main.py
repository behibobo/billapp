import helper

from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_world():
   return 'Hello World!'

@app.route('/item/new', methods = ['POST'])
@cross_origin()
def add_item():
       
   #Get item from the POST body
   req_data = request.get_json()
   item = req_data['item']
   
   #Add item to the list
   res_data = helper.add_to_list(item)

   #Return error if item not added
   if res_data is None:
      response = Response("{'error': 'Item not added - '}"  + item, status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/items/all')
def get_all_items():
   # Get items from the helper
   res_data = helper.get_all_items()
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   return response

@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):
   #Get parameter from the URL
   item_id = id
   
   # Get items from the helper
   item = helper.get_item(id)
   
   #Return 404 if item not found
   if item is None:
      response = Response("{'error': 'Item Not Found - '}"  + item_id, status=404 , mimetype='application/json')
      return response

   #Return status
   res_data = {
      'id': item[0],
      'task': item[1],
      'status': item[2]
   }

   response = Response(json.dumps(res_data), status=200, mimetype='application/json')
   return response

@app.route('/item/<int:id>', methods = ['PUT'])
@cross_origin()
def update_status(id):
   #Get item from the POST body
   req_data = request.get_json()
   task = req_data['task']
   
   #Update item in the list
   res_data = helper.update_status(id, task)
   if res_data is None:
      response = Response("{'error': 'Error updating item'}", status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response

@app.route('/item/<int:id>', methods = ['DELETE'])
def delete_item(id):
   res_data = helper.delete_item(id)
   if res_data is None:
      response = Response("{'error': 'Error deleting item' }", status=400 , mimetype='application/json')
      return response
   
   #Return response
   response = Response(json.dumps(res_data), mimetype='application/json')
   
   return response


if __name__ == "__main__":
   app.run()