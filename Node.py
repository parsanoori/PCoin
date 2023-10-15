import ecdsa
import hashlib
import random
import time
import json
import threading
import socket
import sys
import node_configs

from Transaction import Transaction
from MerkeTree import MerkleTree
from Block import Block
from Peer import Peer

difficulty = 4
port = 5000
peers = []
pending_transactions = []
blockchain: [Block] = []
blockchain_lock = threading.Lock()
pending_transactions_lock = threading.Lock()
peers_lock = threading.Lock()
blockchain.append(Block([]))


# types of messages:
#  - new transaction
#  - new block
#  - new peer


def handle_new_transaction(content: json):
    global pending_transactions
    global pending_transactions_lock
    transaction = Transaction(ecdsa.VerifyingKey.from_string(content['sender_public_key']),
                              ecdsa.SigningKey.from_string(content['sender_signature']),
                              ecdsa.VerifyingKey.from_string(content['receiver_public_key']), content['amount'])
    if transaction.isValid():
        pending_transactions_lock.acquire()
        pending_transactions.append(transaction)
        pending_transactions_lock.release()
        print("New transaction: " + str(transaction))
    else:
        print("Invalid transaction: " + str(transaction))


def handle_new_block(content: json):
    global blockchain
    global blockchain_lock
    block = Block(content['content'], blockchain[-1], content['hash'], content['prevHash'], content['nonce'],
                  content['difficulty'])
    if block.isValid():
        blockchain_lock.acquire()
        blockchain.append(block)
        blockchain_lock.release()
        print("New block: " + str(block))
    else:
        print("Invalid block: " + str(block))


def handle_new_peer(content: json):
    global peers
    global peers_lock
    peers_lock.acquire()
    peers.append(Peer(content['ip'], content['port']))
    peers_lock.release()
    print("New peer: " + content)


def broadcast(message: json):
    global peers
    global peers_lock
    peers_lock.acquire()
    for peer in peers:
        peer.send(message)
    peers_lock.release()


def handle_client(client_sock: socket.socket):
    data = client_sock.recv(1024).decode('utf-8')
    message = json.loads(data)
    if message['type'] == 'new transaction':
        handle_new_transaction(message['content'])
        broadcast(message)
    elif message['type'] == 'new block':
        handle_new_block(message['content'])
        broadcast(message)
    elif message['type'] == 'new peer':
        handle_new_peer(message['content'])
        broadcast(message)
    else:
        print("Invalid message type: " + message['type'])
    client_sock.close()


def do_mining():
    global pending_transactions
    global pending_transactions_lock
    global blockchain
    global blockchain_lock
    global difficulty
    while True:
        pending_transactions_lock.acquire()
        if len(pending_transactions) > 0:
            block = Block(pending_transactions, blockchain[-1], difficulty=difficulty)
            block.mine()
            blockchain_lock.acquire()
            blockchain.append(block)
            blockchain_lock.release()
            pending_transactions = []
        pending_transactions_lock.release()
        # broadcast the blockchain
        broadcast(json.dumps({'type': 'new block', 'content': blockchain[-1].__dict__}))
        time.sleep(1)


def main():
    global port
    global peers
    global pending_transactions
    global blockchain
    global blockchain_lock
    global pending_transactions_lock
    global peers_lock
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    # run the mining thread
    mining_thread = threading.Thread(target=do_mining)
    mining_thread.start()

    # connect to the network
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((node_configs.server_address, port))
    server.listen(5)
    while True:
        client_sock, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_sock,))
        client_thread.start()


if __name__ == '__main__':
    main()
