from kivy.storage.jsonstore import JsonStore

class Counter:
    def __init__(self):
        self.count = JsonStore("animal_count.json")
    
    def modify_stock(self, n):
        if self.count.exists("count"):
            existing = self.count["count"].get("data", 0)
            new = existing + n
            if new >= 0:
                self.count.put("count", data=new)
            else:
                self.count.put("count", data=0)
        else:
            if n >= 0:
                self.count.put("count", data=n)