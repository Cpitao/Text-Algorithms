class HuffmanInternal:

    def __init__(self, left, right, weight):
        self.left = left
        self.right = right
        self.weight = weight

    def __repr__(self):
        res = "internal:" + str(self.weight) + '{\n'
        res += str(self.left) + '}\n{'
        res += str(self.right) + '}'

        return res


class HuffmanLeaf:

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __repr__(self):
        return str(self.value) + ":" + str(self.weight) + '\n'
