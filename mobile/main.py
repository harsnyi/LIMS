from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from page_first import FirstPage
from page_main import MainPage
from page_second import SecondPage

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(FirstPage(name='first'))
        sm.add_widget(SecondPage(name='second'))
        
        return sm

if __name__ == "__main__":
    MyApp().run()