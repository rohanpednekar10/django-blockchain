from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .rocoin import Blockchain
from uuid import uuid4
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# Part 2:  Mining our blockchain

node_address = str(uuid4()).replace('-', '')

# Creating a blockchain
blockchain = Blockchain()

def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        blockchain.add_transaction(sender=node_address, receiver='You', amount=1)
        block = blockchain.create_block(proof, previous_hash)
        response = {
            'message': 'Congratulations, you just mined a block!',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'transactions': block['transactions']
        }
        return JsonResponse(response)

def get_chain(request):
    if request.method == 'GET':
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return JsonResponse(response)

def is_valid(request):
    if request.method == 'GET':
        valid = blockchain.is_chain_valid(blockchain.chain)
        if valid:
            response = {
                'message': 'All good. The Blockchain is valid.'
            }
        else:
            response = {
                'message': 'Houston, we have a problem. The Blockchain is not valid.'
            }
        return JsonResponse(response)

@csrf_exempt
def add_transaction(request):
    if request.method == 'POST':
        received_json = json.loads(request.body)
        transaction_keys = ['sender', 'receiver', 'amount']
        if not all(key in received_json for key in transaction_keys):
            return 'Some elements of the transaction are missing'
        index = blockchain.add_transaction(received_json['sender'], received_json['receiver'], received_json['amount'])
        response = {
            'message': f'This transaction will be added to the block {index}'
        }
        return JsonResponse(response)

@csrf_exempt
def connect_node(request):
    if request.method == 'POST':
        received_json = json.loads(request.body)
        nodes = received_json.get('nodes')
        if nodes is None:
            return 'No Nodes'
        for node in nodes:
            blockchain.add_node(node)
        response = {
            'message': 'All the nodes are now connected. The Rocoin blockchain contains the following nodes:',
            'total_nodes': list(blockchain.nodes)
        }
        return JsonResponse(response)

def replace_chain(request):
    if request.method == 'GET':
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {
                'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'All good. The chain is the largest one.',
                'actual_chain': blockchain.chain
            }
        return JsonResponse(response)