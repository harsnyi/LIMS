from kivy.app import App
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

class MyApp(App):
    def build(self):
        self.storage = Storage()
        
        sm = ScreenManager()
        sm.add_widget(MainPage(self.storage, name='main'))
        sm.add_widget(FeedingScreen(self.storage, name='feeding_screen'))
        sm.add_widget(SaleScreen(self.storage, name='sale_screen'))
        sm.add_widget(EggSaleScreen(self.storage, name='egg_sale_screen'))
        sm.add_widget(ConsumeScreen(self.storage, name='consume_screen'))
        sm.add_widget(HatchingScreen(self.storage, name='hatching_screen'))
        sm.add_widget(OtherExpensesScreen(self.storage, name='other_expenses_screen'))
        sm.add_widget(PerishedScreen(self.storage, name='perished_screen'))
        sm.add_widget(DataScreen(self.storage, name='data_screen'))

        return sm

if __name__ == "__main__":
    MyApp().run()