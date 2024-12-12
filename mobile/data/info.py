from kivy.storage.jsonstore import JsonStore
import numpy as np

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
        error_message = "Nem létezik állomány, kérlek először hozz létre állományt!"
        if self.info.exists("count"):
            existing = self.info["count"].get("data", 0)
            if n > existing:
                error_message = "Nagyobb a megadott érték mint az állományban lévő állatok száma!"
                raise Exception(error_message)
        else:
            raise Exception(error_message)
        
    def get_grain_nutrition_price(self) -> tuple:
        if self.info.exists("prices"):
            grain_price = self.info["prices"]["data"].get("grain_price", np.nan)
            nutrition_price = self.info["prices"]["data"].get("nutrition_price", np.nan)
            if np.nan in [grain_price, nutrition_price]:
                return 0, 0
        
            return grain_price, nutrition_price
        
        return 0, 0
    
    def save_new_prices(self, grain, nutrition):
        new = {"grain_price": grain, "nutrition_price": nutrition }
        self.info.put("prices", data=new)