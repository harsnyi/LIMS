from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

class OtherExpensesScreen(Screen):
    def __init__(self, storage, counter, **kwargs):
        super().__init__(**kwargs)
        self.storage = storage
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(
            text="Other Expenses",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(label)
        
        button = Button(text="Back to Main Page", font_size=24)
        button.bind(on_press=self.go_to_main_page)

        layout.add_widget(button)
        self.add_widget(layout)

    def go_to_main_page(self, instance):
        self.manager.current = 'main'
