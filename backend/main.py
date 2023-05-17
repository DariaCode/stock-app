from flask import Flask
from api.api import api_bp

app = Flask(__name__)

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':  
   app.run(port=5000)
