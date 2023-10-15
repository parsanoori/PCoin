from MerkeTree import MerkleTree
from Transaction import Transaction

difficulty = 4


class Block:
    def __init__(self, content: [Transaction | str], prevBlock: 'Block' = None, hash=None, prevHash=None, nonce=None,
                 difficulty=difficulty):
        self.content = content
        self.prevBlock = prevBlock
        self.merkleTree = MerkleTree(content)
        self.hash = hash
        self.prevHash = prevHash
        self.nonce = nonce
        self.difficulty = difficulty

    def mine(self):
        self.hash = self.merkleTree.root.hash
        self.prevHash = self.prevBlock.hash if self.prevBlock is not None else None
        self.nonce = 0
        while not self.isHashValid():
            self.nonce += 1
            self.hash = self.merkleTree.root.hash
        print("Mined Block: " + str(self))

    def isHashValid(self):
        return self.hash[0:self.difficulty] == "0" * self.difficulty

    def areTransactionsValid(self):
        for transaction in self.content:
            if type(transaction) == str:
                continue
            if not transaction.isValid():
                return False
        return True

    def isValid(self):
        if self.hash is None:
            return False
        if not self.isHashValid():
            return False
        if not self.areTransactionsValid():
            return False
        if self.prevBlock is None:
            return True
        return self.prevBlock.hash == self.prevHash

    def __str__(self):
        return self.hash

    def __repr__(self):
        return self.hash

    def __dict__(self):
        return {
            "content": self.content,
            "hash": self.hash,
            "prevHash": self.prevHash,
            "nonce": self.nonce,
            "difficulty": self.difficulty
        }
