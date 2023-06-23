from flask import Flask, request, jsonify
from .utilities import calculate_overlap
import requests 
from flask import Blueprint

api = Blueprint('api', __name__)

# @api.route('/api/test', methods=['GET'])
# def get_data():
#     data = {'message': 'Hello from the backend!'}
#     return jsonify(data)



@api.route('/api/overlap', methods=['POST'])
def calculate_overlap_api():
    json_data = request.get_json()  # This gets the GeoJSON data from the request body
    if not json_data:
        return {"error": "No GeoJSON data provided"}, 400
    if 'features' not in json_data:
        return {"error": "Invalid GeoJSON data, 'features' key not found"}, 400
    
    # Call calculate_overlap in utilities.py function to calculate the overlap
    overlap_data = calculate_overlap(json_data)

    if "message" in overlap_data and overlap_data["message"] == "No overlap found":
        return overlap_data, 200
        
    if "message" in overlap_data and overlap_data["message"] == "AOI size exceeds limit. Please make your AOI smaller.":
        return {"error": "AOI size exceeds limit. Please make your AOI smaller."}, 200
    # Return the results as JSON
    return jsonify(overlap_data), 200

