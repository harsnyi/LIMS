from kivy.storage.jsonstore import JsonStore

class Information:
    def __init__(self):
        self.info = JsonStore("info.json")
    
    def modify_stock(self, n):
        if self.info.exists("count"):
            existing = self.info["count"].get("data", 0)
            new = existing + n
            if new >= 0:
                self.info.put("count", data=new)
            else:
                self.info.put("count", data=0)
        else:
            if n >= 0:
                self.info.put("count", data=n)
    
    def check_stock(self, n):
        if self.info.exists("count"):
            existing = self.info["count"].get("data", 0)
            if n > existing:
                raise Exception("Nagyobb a megadott érték mint az állományban lévő állatok száma!")
    
    def get_grain_nutrition_price(self) -> tuple:
        grain_price = self.info["prices"].get("grain_price", 0)
        nutrition_price = self.info["prices"].get("nutrition_price", 0)
        if 0 in [grain_price, nutrition_price]:
            return (0, 0)
        
        return (grain_price, nutrition_price)