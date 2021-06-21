class Node:
    def __init__(self, name, content, path, type):
        self.name = name
        self.content = content
        self.items = []
        self.path = path
        self.type = type

    def get_json(self):
        return {"text": self.name, "path": self.path,"type":self.type, "items": [i.get_json() for i in self.items]}