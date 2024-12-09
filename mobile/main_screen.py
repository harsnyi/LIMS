from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class MainPage(Screen):
    def __init__(self, storage, info, **kwargs):
        super().__init__(**kwargs)
        self.storage = storage
        self.information = info

        # Create a ScrollView to enable scrolling
        self.scroll_view = ScrollView(size_hint=(1, 1))

        # BoxLayout inside the ScrollView
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))  # Bind height to content height

        # Create a label at the top
        self.title_label = Label(
            text="LIMS",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5},
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.title_label)

        # Create stock label; initialize it here
        self.stock_label = Label(
            text="Állomány: 0",  # Initialize with a default value
            size_hint=(None, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            padding=(60, 0, 0, 0)
        )
        self.layout.add_widget(self.stock_label)

        # Define button labels and the functions to call
        names = {
            "Napi Etetés": self.jump_to_feeding_screen,
            "Értékesítés": self.jump_to_sale_screen,
            "Tojás Értékesítés": self.jump_to_egg_sale_screen,
            "Saját felhasználás": self.jump_to_consume_screen,
            "Keltetés": self.jump_to_hatching_screen,
            "Egyéb kiadások": self.jump_to_other_expenses_screen,
            "Elhullás": self.jump_to_perished_screen,
            "Adatok": self.jump_to_data_screen
        }

        # Add buttons to the layout
        for key, value in names.items():
            button = Button(
                text=key,
                font_size=24,
                size_hint=(1, None),
                height=180,
                background_color=(0, 0.6, 0.9, 1),
                color=(1, 1, 1, 1),
                background_normal='',
                background_down='',
            )
            button.bind(on_press=value)
            self.layout.add_widget(button)

        self.scroll_view.add_widget(self.layout)

        self.add_widget(self.scroll_view)

    def on_enter(self):
        # Update the stock value every time the screen is entered
        stock = self.information.info.get('count')["data"] if self.information.info.exists('count') else 0
        self.stock_label.text = f"Állomány: {stock}"

    # Screen transition methods
    def jump_to_feeding_screen(self, instance):
        self.manager.current = 'feeding_screen'

    def jump_to_sale_screen(self, instance):
        self.manager.current = 'sale_screen'
    
    def jump_to_egg_sale_screen(self, instance):
        self.manager.current = 'egg_sale_screen'
    
    def jump_to_consume_screen(self, instance):
        self.manager.current = 'consume_screen'
    
    def jump_to_hatching_screen(self, instance):
        self.manager.current = 'hatching_screen'
    
    def jump_to_other_expenses_screen(self, instance):
        self.manager.current = 'other_expenses_screen'
        
    def jump_to_perished_screen(self, instance):
        self.manager.current = 'perished_screen'
        
    def jump_to_data_screen(self, instance):
        self.manager.current = 'data_screen'