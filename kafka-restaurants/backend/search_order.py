from flask import Flask, request, jsonify
import logging
import os
from flask_cors import CORS
import json
from kafka import KafkaProducer
from dotenv import load_dotenv

app = Flask(__name__)
logger = logging.getLogger(__name__)

CORS(app)  # Enable CORS for all routes
app.json.sort_keys = False

ORDER_KAFKA_TOPIC = "order"
load_dotenv()
bootstrap_svr =os.getenv('BOOTSTRAP_SVR')
logger.info("bootstrap server - "+ bootstrap_svr)
producer = KafkaProducer(bootstrap_servers=bootstrap_svr )

# Search for restaurants
@app.route('/search', methods=['GET'])
def search():
    # Load the JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    restaurants_path = os.path.join(current_dir, 'config', 'restaurants.json')
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
     # Send kafka producer
    data = {
        "email": order_data["email"],
        "credit_card": order_data["creditCard"],
        "restaurant": order_data["restaurant"]
    }

    producer.send(ORDER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
    print(f"Done Sending..{data}")

    return jsonify({"message": "Order successfully placed, Wait for confirmation in your mail"}), 200




@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0')