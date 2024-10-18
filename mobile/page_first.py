from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class FirstPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Button to go back to the main page
        button = Button(text="Back to Main Page", font_size=24)
        button.bind(on_press=self.go_to_main_page)

        layout.add_widget(button)
        self.add_widget(layout)

    def go_to_main_page(self, instance):
        # Switch back to the Main Page
        self.manager.current = 'main'
