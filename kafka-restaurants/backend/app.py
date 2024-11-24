from flask import Flask, request, jsonify, render_template
import logging
from datetime import datetime
import os
from flask_cors import CORS
import json


logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.json.sort_keys = False

# Search for restaurants that is open now with optional parameters eg /search?restaurantStyle=italian?vegetarian=true
@app.route('/search', methods=['GET'])
def search():
    # get the json file 
    restaurants_path = 'restaurants.json'
    with open(restaurants_path, 'r') as file:
        data = json.load(file)
    print (data)
    restaurant_name = request.args.get('restaurantName')
    restaurant_style = request.args.get('restaurantStyle')
    vegetarian = request.args.get('vegetarian')
    deliveries = request.args.get('deliveries')

    try:
        results = [
         {
            "name": "Pizza Palace",
            "style": "Italian",
            "vegetarian": True,
            "delivery": True
         },
         {
            "name": "shawarma",
            "style": "Italian",
            "vegetarian": True,
            "delivery": True
         }
        ]
        return jsonify(results), 200
    except Exception as e:
      return jsonify({"message": f"Failed to retrieve records: {str(e)}"}), 500

#Search by restaurantName /searchByRest?restaurantName=pizza
#@app.route('/searchByRest', methods=['GET'])
#def searchsimple():
# restaurant_name = request.args.get('restaurantName', type=str)
# query = "SELECT * FROM restaurantTable WHERE restaurantName = ?"
# params = [restaurant_name]
# try:
#        conn = get_db_connection()
#        cursor = conn.cursor()
#        cursor.execute(query, params)
#        records = cursor.fetchall()
#        results = [
#            {
#                "restaurantName": row.restaurantName,
#                "restaurantStyle": row.restaurantStyle,
#                "vegetarian": row.vegetarian,
#                "deliveries": row.deliveries,
#                "timeOpen": str(row.timeOpen)[:-3],
#                "timeClose": str(row.timeClose)[:-3]
#
#            }for row in records]
#        
#        conn.close()
#        return jsonify(results), 200
# except Exception as e:
#      return jsonify({"message": f"Failed to retrieve records: {str(e)}"}), 500 
#
#app_user = os.environ["APP_USER"]
#app_pass = os.environ["APP_PASS"]

if __name__ == '__main__':
    app.run(host='0.0.0.0')