from kivy.storage.jsonstore import JsonStore

class Storage():
    def __init__(self):
        self.data = JsonStore('data.json')
    
    def add_item(self, key, item_key, item: dict):
        if self.data.exists(key):
            retrieved_data = self.data.get(key)['data']
            
            retrieved_data[item_key] = item
            self.data.put(key, data=retrieved_data)
        else:
            self.data.put(key, data={item_key: item})
    
    def already_exists(self, date, key) -> bool:
        if date in self.data and self.data[date]["data"].get(key):
            return True
        
        return False
    
    def modify_stock(self, n):
        if self.data.exists("stock"):
            new = int(self.data["stock"]["count"]) + n
            if new >= 0:
                self.data.put("stock", count=new)
            else:
                self.data.put("stock", count=0)
        else:
            if n >= 0:
                self.data.put("stock", count=n)

    def list(self):
        pass