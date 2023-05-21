import json
from flask import Flask, jsonify
from flask_cors import CORS
from api.api import api_bp
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))
    
# Enable CORS for all routes
CORS(app, origins=['http://localhost:8080', 'http://192.168.86.37:8080'])
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
# CORS(app)

if __name__ == '__main__':
    app.run(port=5000)
