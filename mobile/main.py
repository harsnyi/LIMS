from kivy.uix.screenmanager import ScreenManager
from screens.feeding_screen import FeedingScreen
from main_screen import MainPage
from screens.sale_screen import SaleScreen
from screens.egg_sale_screen import EggSaleScreen
from screens.consume_screen import ConsumeScreen
from screens.hatching_screen import HatchingScreen
from screens.other_expenses_screen import OtherExpensesScreen
from screens.perished_screen import PerishedScreen
from screens.data_screen import DataScreen
from data.storage import Storage
from data.counter import Counter
from kivymd.app import MDApp

class MyApp(MDApp):
    def build(self):
        self.storage = Storage()
        self.counter = Counter()
        
        sm = ScreenManager()
        sm.add_widget(MainPage(self.storage, self.counter, name='main'))
        sm.add_widget(FeedingScreen(self.storage, self.counter, name='feeding_screen'))
        sm.add_widget(SaleScreen(self.storage, self.counter, name='sale_screen'))
        sm.add_widget(EggSaleScreen(self.storage, self.counter, name='egg_sale_screen'))
        sm.add_widget(ConsumeScreen(self.storage, self.counter, name='consume_screen'))
        sm.add_widget(HatchingScreen(self.storage, self.counter, name='hatching_screen'))
        sm.add_widget(OtherExpensesScreen(self.storage, self.counter, name='other_expenses_screen'))
        sm.add_widget(PerishedScreen(self.storage, self.counter, name='perished_screen'))
        sm.add_widget(DataScreen(self.storage, self.counter, name='data_screen'))

        return sm

if __name__ == "__main__":
    MyApp().run()