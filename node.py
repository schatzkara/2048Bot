
class Node:
    def __init__(self, label, value, sum, parent=None, children=[]):
        self.label = label
        self.value = value
        self.sum = sum
        self.parent = parent
        self.children = children

    def get_label(self):
        return self.label

    def get_value(self):
        return self.value

    def get_sum(self):
        return self.sum

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def add_child(self, child):
        self.children.append(child)

    def print(self):
        result = self.label + ":"
        for child in self.children:
            result += child.get_label() + ','

        return result [:-1]
