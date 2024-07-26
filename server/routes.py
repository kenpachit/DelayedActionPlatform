import os
import json
from flask import Flask, request, jsonify
from datetime import datetime
import pymongo
from bson import ObjectId
from pymongo.errors import PyMongo0error
import logging

app = Flask(__name__)

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'DelayedActionPlatform')

mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client[DB_NAME]
actions_collection = db.actions
schedules_collection = db.schedules
users_collection = db.users

logging.basicConfig(level=logging.INFO)

def is_valid_object_id(object_id):
    try:
        ObjectId(object_id)
        return True
    except:
        return False

@app.errorhandler(PyMongoError)
def handle_mongo_error(error):
    logging.error(f"A MongoDB error occurred: {error}")
    return jsonify(error="A database error occurred"), 500

@app.errorhandler(ValueError)
def handle_value_error(error):
    logging.error(f"A Value error occurred: {error}")
    return jsonify(error="A value error occurred, possibly due to a bad ObjectId"), 400

@app.route('/actions', methods=['POST'])
def create_action():
    action_data = request.json
    action_data['created_at'] = datetime.utcnow()
    try:
        action_id = actions_collection.insert_one(action_data).inserted_id
        return jsonify({'id': str(action_id)}), 201
    except PyMongoError as error:
        return handle_mongo_error(error)

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
    except PyMongoError as error:
        return handle_mongo_error(error)

@app.route('/actions/<action_id>', methods=['PUT'])
def update_action(action_id):
    if not is_valid_object_id(action_id):
        return jsonify({'error': 'Invalid action ID format'}), 400
    updated_action_data = request.json
    try:
        update_result = actions_collection.update_one({'_id': ObjectId(action_id)}, {'$set': updated_action_data})
        if update_result.matched_count:
            return jsonify({'message': 'Action updated successfully'}), 200
        else:
            return jsonify({'error': 'Action not found'}), 404
    except PyMongoError as error:
        return handle_mongo_error(error)

@app.route('/actions/<action_id>', methods=['DELETE'])
def delete_action(action_id):
    if not is_valid_object_id(action_id):
        return jsonify({'error': 'Invalid action ID format'}), 400
    try:
        delete_result = actions_collection.delete_one({'_id': ObjectId(action_id)})
        if delete_result.deleted_count:
            return jsonify({'message': 'Action deleted successfully'}), 200
        else:
            return jsonify({'error': 'Action not found'}), 404
    except PyMongoError as error:
        return handle_mongo_error(error)

if __name__ == '__main__':
    app.run(debug=True)