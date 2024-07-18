from flask import Flask, request, jsonify
from flask_caching import Cache
from web3 import Web3
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# Configure cache
app.config['CACHE_TYPE'] = 'simple'  # Consider using 'redis' in production for better performance
cache = Cache(app)

blockchain_provider = os.getenv("BLOCKCHAIN_PROVIDER")
chain_id = int(os.getenv("CHAIN_ID"))
contract_address = Web3.toChecksumAddress(os.getenv("CONTRACT_ADDRESS"))
abi_path = 'path_to_Abi.json'

web3 = Web3(Web3.HTTPProvider(blockchain_provider))

# Load ABI just once if it doesn't change often
with open(abi_path) as f:
    abi = json.load(f)
contract = web3.eth.contract(address=contract_address, abi=abi)

@app.route('/api/actions', methods=['POST'])
def schedule_action():
    data = request.json
    errors = validate_action_data(data)
    if errors:
        return jsonify({'status': 'error', 'message': errors}), 400

    account = data.get('account')
    privateKey = data.get('privateKey')
    action = data.get('action')
    args = data.get('args', [])
    
    nonce = web3.eth.getTransactionCount(account)
    tx = contract.functions.triggerAction(action, *args).buildTransaction({
        'chainId': chain_id,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    signed_tx = web3.eth.account.signTransaction(tx, privateKey)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return jsonify({'status': 'success', 'data': {'txHash': tx_hash.hex()}}), 200

@app.route('/api/schedules', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_schedules():
    account = request.args.get('account')
    
    if not account:
        return jsonify({'status': 'error', 'message': 'Account parameter is required'}), 400
    
    schedules = contract.functions.getSchedules(account).call()

    return jsonify({'status': 'success', 'data': schedules}), 200

@app.route('/api/users', methods=['POST', 'GET'])
def manage_users():
    if request.method == 'POST':
        data = request.json
        username = data.get("username")
        
        if not username:
            return jsonify({'status': 'error', 'message': 'Username is required'}), 400

        return jsonify({'status': 'success', 'data': {'username': username, 'message': 'User created successfully'}}), 201

    elif request.method == 'GET':
        users = [{'username': 'example_user'}]
        return jsonify({'status': 'success', 'data': users}), 200

def validate_action_data(data):
    if 'account' not in data or 'privateKey' not in data or 'action' not in data:
        return "Account, privateKey, and action fields are required"
    return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)