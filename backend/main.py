import json
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from api.api import api_bp
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = 'https://stock-market-21052023.ew.r.appspot.com/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_frontend(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
