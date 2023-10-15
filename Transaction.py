import ecdsa
import hashlib
import random
import time
import json


class Transaction:
    def __init__(self, seder_public_key: ecdsa.VerifyingKey, sender_signature: ecdsa.SigningKey,
                 receiver_public_key: ecdsa.VerifyingKey, amount: int):
        self.sender_public_key = seder_public_key
        self.sender_signature = sender_signature
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.timestamp = time.time()
        self.hash = self.calculateHash()

    def calculateHash(self):
        return hashlib.sha256((str(self.sender_public_key) + str(self.receiver_public_key) + str(self.amount) + str(
            self.timestamp)).encode('utf-8')).hexdigest()

    def isValid(self):
        if self.sender_public_key is None:
            return True
        return self.sender_public_key.verify(self.sender_signature, self.hash.encode('utf-8'))

    def __str__(self):
        return self.hash

    def __repr__(self):
        return self.hash

    def __dict__(self):
        return {
            "sender_public_key": str(self.sender_public_key),
            "sender_signature": str(self.sender_signature),
            "receiver_public_key": str(self.receiver_public_key),
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.hash
        }
