from Transaction import Transaction
import ecdsa
import socket
import json

known_nodes = [('localhost', 5000)]
pending_transactions = []


def broadcast(message: Transaction):
    for node in known_nodes:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(node)
        s.sendall(json.dumps({'type': 'new transaction', 'content': message.__dict__}).encode('utf-8'))
        s.close()


def new_transaction(sender_public_key: ecdsa.VerifyingKey, sender_signature: ecdsa.SigningKey,
                    receiver_public_key: ecdsa.VerifyingKey, amount: int):
    transaction = Transaction(sender_public_key, sender_signature, receiver_public_key, amount)
    pending_transactions.append(transaction)
    broadcast(transaction)


def get_pending_transactions():
    return pending_transactions


def main():
    private_key = ecdsa.SigningKey.generate()
    public_key = private_key.get_verifying_key()
    print("Welcome to the client")
    print("Commands:")
    print("1. new transaction")
    print("2. exit")
    while True:
        command = input("Enter command: ")
        if command == "new transaction":
            receiver_public_key = input("Enter receiver public key: ")
            receiver_public_key = ecdsa.VerifyingKey.from_string(receiver_public_key)
            amount = int(input("Enter amount: "))
            new_transaction(public_key, private_key, receiver_public_key, amount)
        elif command == "exit":
            break
        else:
            print("Invalid command")


if __name__ == '__main__':
    main()
