class DataSet:
    def __init__(self):
        self.reset()

    def save(self, key, data):
        if key in self.data.keys():
            raise("This data key is already used")
        else:
            self.data[key] = data

    def reset(self):
        self.data = {}