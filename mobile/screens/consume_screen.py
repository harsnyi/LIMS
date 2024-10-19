from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

class ConsumeScreen(Screen):
    def __init__(self, storage, **kwargs):
        super().__init__(**kwargs)
        self.storage = storage

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        label = Label(
            text="Consume",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1)
        )
        layout.add_widget(label)

        self.count_input = TextInput(
            hint_text="Enter count of consumed animals",
            multiline=False,
            size_hint=(1, None),
            height=100
        )
        layout.add_widget(self.count_input)

        self.date_input = TextInput(
            hint_text="Enter date (YYYY-MM-DD)",
            multiline=False,
            size_hint=(1, None),
            height=100
        )
        layout.add_widget(self.date_input)

        button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=180)
        
        back_button = Button(text="Vissza",
                            font_size=24,
                            size_hint=(1, None),
                            height=180,
                            background_color=(1, 0.75, 0.4, 1),
                            color=(1, 1, 1, 1),
                            background_normal='',
                            background_down='',)
        back_button.bind(on_press=self.go_to_main_page)
        button_layout.add_widget(back_button)
        
        save_button = Button(text="Mentés",
                            font_size=24,
                            size_hint=(1, None),
                            height=180,
                            background_color=(0.54, 0.75, 0.64, 1),
                            color=(1, 1, 1, 1),
                            background_normal='',
                            background_down='',)
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)

        self.add_widget(scroll_view)

    def go_to_main_page(self, instance):
        self.manager.current = 'main'
