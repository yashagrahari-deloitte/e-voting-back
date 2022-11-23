import datetime
import hashlib 
import json

class Blockchain(object):

    def __init__(self):
       self.chain = []
       self.current_transactions = []
       self.new_block(previous_hash=1, proof=100)

    def proof_of_work(self, last_proof):
       """This method is where you the consensus algorithm is implemented.
       It takes two parameters including self and last_proof"""
       proof = 0
       while self.valid_proof(last_proof, proof) is False:
           proof +=1
       return proof

    @staticmethod
    def valid_proof(last_proof, proof):
       """This method validates the block"""
       guess = f'{last_proof}{proof}'.encode()
       guess_hash = hashlib.sha256(guess).hexigest()
       return guess_hash[:4] == "0000"

    def new_block(self, proof, previous_hash=None):
       #This function creates new blocks and then adds to the existing chain
       """This method will contain two parameters proof, previous hash"""
       block = {
           'index': len(self.chain) + 1,
           'timestamp' : str(datetime.datetime.now()),
           'proof': proof,
           'previous_hash': previous_hash or self.hash(self.chain[-1]),

       }
       # Set the current transaction list to empty.
       self.current_transactions=[]
       self.chain.append(block)
       return block

    def new_transaction(self):
       #This function adds a new transaction to already existing transactions
       """This will create a new transaction which will be sent to the next block. It will contain
       three variables including sender, recipient and amount
       """
       self.current_transactions.append(
           {
               'candidate_id': 1,
               'party_id': 1,
           }
       )
       return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
       #Used for hashing a block
       """The follow code will create a SHA-256 block hash and also ensure that the dictionary is ordered"""
       block_string = json.dumps(block, sort_keys=True).encode()
       return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
       # Calls and returns the last block of the chain
       return self.chain[-1]
     
    