# A merkle tree implementation
import hashlib
from Transaction import Transaction


def str_to_hash(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def transaction_to_hash(content: Transaction) -> str:
    return content.hash


def content_to_hash(content) -> str:
    if type(content) == str:
        return str_to_hash(content)
    if type(content) == Transaction:
        return transaction_to_hash(content)
    raise Exception("Invalid content type")


class MerkleNode:
    def __init__(self, left, right, content: str | Transaction):
        self.left = left
        self.right = right
        self.content = content
        if left is None and right is None:
            self.hash = content_to_hash(content)
        else:
            self.hash = content_to_hash(left.hash + right.hash)

    def __str__(self):
        return self.content

    def copy(self):
        return MerkleNode(self.left, self.right, self.content)


class MerkleTree:
    def __init__(self, content: [Transaction | str]):
        self.content = content
        content = [MerkleNode(None, None, e) for e in content]
        self.root = self.buildTree(content)

    def buildTree(self, content: [MerkleNode]):
        if len(content) % 2 == 1:
            content.append(content[-1].copy())
        if len(content) == 2:
            return MerkleNode(content[0], content[1], content[0].content + content[1].content)
        half = len(content) // 2
        left = self.buildTree(content[:half])
        right = self.buildTree(content[half:])
        return MerkleNode(left, right, left.content + right.content)

    def __str__(self) -> str:
        return self.traverse(self.root)[0:-1]

    def traverse(self, node: MerkleNode) -> str:
        if node is None:
            return ""
        res = node.content + "\n"
        res += self.traverse(node.left)
        res += self.traverse(node.right)
        return res

    def print(self):
        self.printHelper(self.root)

    def printHelper(self, node: MerkleNode):
        if node is None:
            return
        print(node)
        self.printHelper(node.left)
        self.printHelper(node.right)


def main(content):
    tree = MerkleTree(content)
    tree.print()
    print(tree.root.hash)


if __name__ == "__main__":
    user_input = input().split(" ")
    main(user_input)
