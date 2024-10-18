from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label

class MainPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text="LIMS",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(label)
        
        names = {
            "Go to Page 1":self.go_to_first_page,
            "Go to Page 2":self.go_to_second_page
        }
        for key, value in names.items():
            button = Button(
                text=key,
                font_size=24,
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                background_color=(0, 0.6, 0.9, 1),
                color=(1, 1, 1, 1),
                border=(0, 0, 0, 0),
                background_normal='',
                background_down='',
            )
            button.bind(on_press=value)
            layout.add_widget(button)
        
        self.add_widget(layout)

    def go_to_first_page(self, instance):
        self.manager.current = 'first'

    def go_to_second_page(self, instance):
        self.manager.current = 'second'