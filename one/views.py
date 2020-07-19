from django.shortcuts import render
from django.http import JsonResponse
from .blockchain import Blockchain
# Create your views here.

# Part 2:  Mining our blockchain

# Creating a blockchain
blockchain = Blockchain()

def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
        response = {
            'message': 'Congratulations, you just mined a block!',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
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

