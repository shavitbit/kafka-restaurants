from flask import Flask, request, jsonify
import logging
import os
from flask_cors import CORS
import json


logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.json.sort_keys = False

# Search for restaurants
@app.route('/search', methods=['GET'])
def search():
    # Load the JSON file
    restaurants_path = 'restaurants.json'
    with open(restaurants_path, 'r') as file:
        data = json.load(file)

    # Retrieve query parameters
    name = request.args.get('restaurant_name', '').lower()
    style = request.args.get('restaurant_style', '').lower()
    vegetarian = request.args.get('vegetarian', '').lower() == 'true'  # Convert to boolean

    # Filter based on given criteria
    filtered_restaurants = []
    for restaurant in data:
        # Apply filters
        if name and name not in restaurant["name"].lower():
            continue
        if style and style != restaurant["style"].lower():
            continue
        if vegetarian and not restaurant["vegetarian"]:
            continue

        # If all filters pass, add the restaurant to the result
        filtered_restaurants.append(restaurant)

    return jsonify(filtered_restaurants), 200
   
@app.route('/orders', methods=['POST'])
def place_order():
    order_data = request.json
    print("Received Order:", order_data)
    return jsonify({"message": "Order successfully placed"}), 200 

    # Mock processing
    if order_data.get('creditCard') and len(order_data['creditCard']) == 16:
        return jsonify({"message": "Order successfully placed"}), 200
    else:
        return jsonify({"message": "Invalid credit card number"}), 400





if __name__ == '__main__':
    app.run(host='0.0.0.0')