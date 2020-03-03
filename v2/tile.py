
class Tile:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.last_merged = 0

    def get_value(self):
        return self.value

    def get_position(self):
        return self.x, self.y

    def get_last_merged(self):
        return self.last_merged

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def merge(self, turn):
        self.value = self.value * 2
        self.last_merged = turn
        return self.value
