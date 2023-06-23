# from app import app
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.views import api


app = Flask(__name__)

CORS(app, origins='http://localhost:3000')


app.register_blueprint(api)


if __name__ == "__main__":
  app.run(debug=True, port=5001)


