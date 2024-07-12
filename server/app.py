from flask import Flask, request, jsonify
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

web3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PROVIDER")))

contract_address = web3.toChecksumAddress(os.getenv("CONTRACT_ADDRESS"))
with open('path_to_Abi.json') as f:
    abi = f.read()
contract = web3.eth.contract(address=contract_address, abi=abi)

@app.route('/api/actions', methods=['POST'])
def schedule_action():
    data = request.json
    account = data.get('account')
    privateKey = data.get('privateKey')
    action = data.get('action')
    args = data.get('args', [])
    
    nonce = web3.eth.getTransactionCount(account)
    tx = contract.functions.triggerAction(action, *args).buildTransaction({
        'chainId': int(os.getenv("CHAIN_ID")),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    signed_tx = web3.eth.account.signTransaction(tx, privateKey)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return jsonify({'status': 'success', 'data': {'txHash': tx_hash.hex()}}), 200

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    account = request.args.get('account')
    
    schedules = contract.functions.getSchedules(account).call()

    return jsonify({'status': 'success', 'data': schedules}), 200

@app.route('/api/users', methods=['POST', 'GET'])
def manage_users():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        
        return jsonify({'status': 'success', 'data': {'username': username, 'message': 'User created successfully'}}), 201

    elif request.method == 'GET':
        users = [{'username': 'example_user'}]
        return jsonify({'status': 'success', 'data': users}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)