#!/bin/bash

# Check if URL is set, else use a default value
API_URL=${API_URL:-http://127.0.0.1:5000}

# Replace the URL in your JavaScript file
sed -i "s|const url = 'http://127.0.0.1:5000';|const url = '${API_URL}';|" /usr/share/nginx/html/script.js
sed -i "s|const url = 'http://127.0.0.1:5000';|const url = '${API_URL}';|" /usr/share/nginx/html/orders.html

# Start Nginx
nginx -g "daemon off;"