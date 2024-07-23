import os
import json
from flask import Flask, request, jsonify
from datetime import datetime
import pymongo
from bson import ObjectId
from pymongo.errors import PyMongoError
import logging

app = Flask(__name__)

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'DelayedActionPlatform')

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
actions_collection = db.actions
schedules_collection = db.schedules
users_collection = db.users

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Helper function to validate ObjectId
def is_valid_object_id(id):
    try:
        ObjectId(id)
        return True
    except:
        return False

@app.errorhandler(PyMongoError)
def handle_mongo_error(e):
    """Handle MongoDB errors globally"""
    logging.error(f"A MongoDB error occurred: {e}")
    return jsonify(error="A database error occurred"), 500

@app.errorhandler(ValueError)
def handle_value_error(e):
    """Handle Value Errors"""
    logging.error(f"A Value error occurred: {e}")
    return jsonify(error="A value error occurred, possibly bad ObjectId"), 400

@app.route('/actions', methods=['POST'])
def create_action():
    data = request.json
    data['created_at'] = datetime.utcnow()
    try:
        action_id = actions_collection.insert_one(data).inserted_id
        return jsonify({'id': str(action_id)}), 201
    except PyMongoError as e:
        return handle_mongo_error(e)

@app.route('/actions/<action_id>', methods=['GET'])
def get_action(action_id):
    if not is_valid_object_id(action_id):
        return jsonify({'error': 'Invalid action ID format'}), 400
    try:
        action = actions_collection.find_one({'_id': ObjectId(action_id)})
        if action:
            action['_id'] = str(action['_id'])
            return jsonify(action), 200
        else:
            return jsonify({'error': 'Action not found'}), 404
    except PyMongoError as e:
        return handle_mongo_error(e)

@app.route('/actions/<action_id>', methods=['PUT'])
def update_action(action_id):
    if not is_valid_object_id(action_id):
        return jsonify({'error': 'Invalid action ID format'}), 400
    data = request.json
    try:
        result = actions_collection.update_one({'_id': ObjectId(action_id)}, {'$set': data})
        if result.matched_count:
            return jsonify({'message': 'Action updated successfully'}), 200
        else:
            return jsonify({'error': 'Action not found'}), 404
    except PyMongoError as e:
        return handle_mongo_error(e)

@app.route('/actions/<action_id>', methods=['DELETE'])
def delete_action(action_id):
    if not is_valid_object_id(action_id):
        return jsonify({'error': 'Invalid action ID format'}), 400
    try:
        result = actions_collection.delete_one({'_id': ObjectId(action_id)})
        if result.deleted_count:
            return jsonify({'message': 'Action deleted successfully'}), 200
        else:
            return jsonify({'error': 'Action not found'}), 404
    except PyMongoError as e:
        return handle_mongo_error(e)

if __name__ == '__main__':
    app.run(debug=True)