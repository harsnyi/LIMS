from kivy.storage.jsonstore import JsonStore

class Storage():
    def __init__(self):
        self.data = JsonStore('data.json')
    
    def list(self):
        pass