from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivymd.uix.pickers import MDDatePicker
from data.storage import Storage
from datetime import datetime

class ConsumeScreen(Screen):
    def __init__(self, storage, **kwargs):
        super().__init__(**kwargs)
        self.storage: Storage = storage
        self.consumed_animals = 0
        self.selected_date = datetime.today().strftime("%Y-%m-%d")

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        label = Label(
            text="Consume",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1)
        )
        layout.add_widget(label)

        label = Label(
            text="Add meg a mennyiséget",
            size_hint=(1, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            
        )
        layout.add_widget(label)
        
        self.count_input = TextInput(
            hint_text="Enter count of consumed animals",
            input_filter='int',
            multiline=False,
            size_hint=(1, None),
            height=100
        )
        layout.add_widget(self.count_input)

        label = Label(
            text="Add meg a dátumot(mai dátum az alapértelmezett)",
            size_hint=(1, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            
        )
        layout.add_widget(label)
        self.date_button = Button(
            text="Válassz dátumot",
            size_hint=(1, None),
            height=100
        )
        self.date_button.bind(on_press=self.show_date_picker)
        layout.add_widget(self.date_button)

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
        save_button.bind(on_press=self.save_consume)
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)

        self.add_widget(scroll_view)

    def show_date_picker(self, instance):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance, value, date_range):
        self.selected_date = value.strftime("%Y-%m-%d")
        self.date_button.text = self.selected_date

    def go_to_main_page(self, instance):
        self.manager.current = 'main'
    
    def save_consume(self, instance):
        try:
            quantity = int(self.count_input.text)
            date = self.selected_date
            if quantity and date and quantity != 0:
                if self.storage.data.exists(date) and "consumed" in self.storage.data[date]:
                    new = int(self.storage.data[date]["consumed"]) + quantity
                    self.storage.data.put(date, consumed=new)    
                else:
                    self.storage.data.put(date, consumed=quantity)
                    
                self.storage.modify_stock(-1 * quantity)
                self.manager.current = 'main'
        except Exception as e:
            print(f"Hiba adódott a mentéskor: {e}")