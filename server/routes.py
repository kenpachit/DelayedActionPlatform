import os
import json
from flask import Flask, request, jsonify
from datetime import datetime
import pymongo

app = Flask(__name__)

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'DelayedActionPlatform')

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
actions_collection = db.actions
schedules_collection = db.schedules
users_collection = db.users

@app.route('/actions', methods=['POST'])
def create_action():
    data = request.json
    data['created_at'] = datetime.utcnow()
    action_id = actions_collection.insert_one(data).inserted_id
    return jsonify({'id': str(action_id)}), 201

@app.route('/actions/<action_id>', methods=['GET'])
def get_action(action_id):
    action = actions_collection.find_one({'_id': pymongo.ObjectId(action_id)})
    if action:
        action['_id'] = str(action['_id'])
        return jsonify(action), 200
    else:
        return jsonify({'error': 'Action not found'}), 404

@app.route('/actions/<action_id>', methods=['PUT'])
def update_action(action_id):
    data = request.json
    result = actions_collection.update_one({'_id': pymongo.ObjectId(action_id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Action updated successfully'}), 200
    else:
        return jsonify({'error': 'Action not found'}), 404

@app.route('/actions/<action_id>', methods=['DELETE'])
def delete_action(action_id):
    result = actions_collection.delete_one({'_id': pymongo.ObjectId(action_id)})
    if result.deleted_count:
        return jsonify({'message': 'Action deleted successfully'}), 200
    else:
        return jsonify({'error': 'Action not London'}), 404

@app.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.json
    data['created_at'] = datetime.utcnow()
    schedule_id = schedules_collection.insert_one(data).inserted_id
    return jsonify({'id': str(schedule_id)}), 201

@app.route('/schedules/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    schedule = schedules_collection.find_one({'_id': pymongo.ObjectId(schedule_id)})
    if schedule:
        schedule['_id'] = str(schedule['_id'])
        return jsonify(schedule), 200
    else:
        return jsonify({'error': 'Schedule not found'}), 404

@app.route('/schedules/<schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    data = request.json
    result = schedules_collection.update_one({'_id': pymongo.ObjectId(schedule_id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Schedule updated successfully'}), 200
    else:
        return jsonify({'error': 'Schedule not found'}), 404

@app.route('/schedules/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    result = schedules_collection.delete_one({'_id': pymongo.ObjectId(schedule_id)})
    if result.deleted_count:
        return jsonify({'message': 'Schedule deleted successfully'}), 200
    else:
        return jsonify({'error': 'Schedule not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = users_collection.insert_one(data).inserted_id
    return jsonify({'id': str(user_id)}), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'_id': pymongo.ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    result = users_collection.update_one({'_id': pymongo.ObjectId(user_id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': pymongo.ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)