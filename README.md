# PCoin Implementation in Python
## Introduction
PCoin is an academical Proof of Work based cryptocurrency implementation in Python. It is based on the Bitcoin protocol
and is intended to be used for educational purposes only. It is not intended to be used in production environments. 
  
The mechanism of PCoin is similar to Bitcoin. It uses the same elliptic curve cryptography and the same hashing algorithm.
The main difference is that PCoin uses a simplified version of the Bitcoin protocol. It is a peer-to-peer system and it 
uses a blockchain to maintain the data it needs.

## The Blockchain
The blockchain is a data structure that contains all the transactions that have been made in the system. It is a linked 
list that contains blocks. Each block contains a list of transactions and a reference to the previous block. The first
block of the blockchain is called the genesis block. The genesis block is the only block that does not have a previous
block. The genesis block is created when the blockchain is created. The genesis block is created by the system.

## The Transactions
A transaction is a data structure that contains information about a transfer of PCoins from one user to another. A
transaction contains the public key of the sender, the public key of the receiver and the amount of PCoins that are
transferred. A transaction also contains a signature that is created by the sender. The signature is created by signing
the transaction with the private key of the sender. The signature is used to verify that the transaction was created by
the sender. The signature is also used to verify that the transaction was not modified by a third party.

## The Proof of Work
The proof of work is a mechanism that is used to prevent double spending. The proof of work is a mathematical puzzle that
is solved by the miners. The miners are the users that are responsible for creating new blocks. The miners are rewarded
with PCoins for solving the puzzle. The puzzle is solved by finding a hash that starts with a certain number of zeros.

## The protocol
The protocol is a set of rules that are used to communicate between the nodes. The protocol is used to send transactions
between the nodes. The protocol is also used to send blocks between the nodes. We used JSON to encode the messages that
are sent between the nodes. One of elements of the JSON message is the type of the message. The type of the message is
used to determine how the message should be handled. The other elements of the JSON message are the data that is sent. 
The type of the message is either: `new transaction`, `new block`, `new peer`. Now we dicuss the body of the message.

### New Transaction
The body contains the followings:
- `send_public_key`: The public key of the sender.
- `sender_signature`: The signature of the sender.
- `receive_public_key`: The public key of the receiver.
- `amount`: The amount of PCoins that are transferred.

### New Block
The body contains the followings:
- `content`: The transactions and the strings.
- `hash`: The hash of the block.
- `previous_hash`: The hash of the previous block.
- `nonce`: The nonce of the block.
- `difficulty`: The difficulty of the block.

### New Peer
The body contains the followings:
- `ip`: The IP address of the peer.
- `port`: The port of the peer.

## To use the system
Run the `node.py` multiple times. The first node will be the genesis node. The other nodes will connect to the genesis
node.
Run the `client.py` to send transactions to the nodes.
