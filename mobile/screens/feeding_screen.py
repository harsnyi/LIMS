from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from data.info import Information
from datetime import datetime

class FeedingScreen(Screen):
    def __init__(self, storage, info, **kwargs):
        super().__init__(**kwargs)
        self.storage = storage
        self.info: Information = info
        self.selected_date = datetime.today().strftime("%Y-%m-%d")
        self.grain_price, self.nutrition_price = self.info.get_grain_nutrition_price()
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))


        title = Label(
            text="Feed Screen",
            size_hint=(1, None),
            height=50,
            color=(0, 0, 0, 1),
            font_size=24
        )
        layout.add_widget(title)

        label = Label(
            text="Add meg a vödrök számát",
            size_hint=(1, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            
        )
        layout.add_widget(label)
        
        self.quantity_input = TextInput(
            hint_text="Ide írd be a mennyiséget",
            multiline=False,
            size_hint=(1, None),
            height=100,
            input_filter="int"
        )
        layout.add_widget(self.quantity_input)

        # Price Inputs
        price_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        
        label = Label(
            text="Gabona ár:",
            size_hint=(0.5, None),
            size=(20, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            
        )
        price_box.add_widget(label)
        
        self.grain_price_input = TextInput(
            text=str(self.grain_price),
            multiline=False,
            size_hint=(0.5, None),
            height=50,
            input_filter="int"
        )
        price_box.add_widget(self.grain_price_input)

        price_box_2 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        
        label = Label(
            text="Táp ár",
            size_hint=(0.5, None),
            size=(20, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
        )
        price_box_2.add_widget(label)
        
        self.nutrition_price_input = TextInput(
            text=str(self.nutrition_price),
            multiline=False,
            size_hint=(0.5, None),
            height=50,
            input_filter="int"
        )
        
        price_box_2.add_widget(self.nutrition_price_input)

        layout.add_widget(price_box)
        layout.add_widget(price_box_2)

        layout.add_widget(Label(text="Válaszd ki mit kaptak", size_hint=(1, None), height=30))
        self.food_type_spinner = Spinner(
            text="Gabona",
            values=["Gabona", "Táp"],
            size_hint=(1, None),
            height=100
        )
        layout.add_widget(self.food_type_spinner)

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
            text=self.selected_date,
            size_hint=(1, None),
            height=100
        )
        self.date_button.bind(on_press=self.show_date_picker)
        layout.add_widget(self.date_button)

        # Buttons
        button_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=180)
        save_button = Button(
            text="Hozzáad",
            size_hint=(1, None),
            background_color=(0, 0.7, 0, 1),
            color=(1, 1, 1, 1)
        )
        save_button.bind(on_press=self.save_feed_data)
        button_box.add_widget(save_button)

        back_button = Button(
            text="Vissza",
            size_hint=(1, None),
            background_color=(0.7, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.go_back)
        button_box.add_widget(back_button)

        layout.add_widget(button_box)

        # Add scrollable view
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

    def save_feed_data(self, instance):
        try:
            quantity = int(self.quantity_input.text)
            grain_price = int(self.grain_price_input.text)
            nutrition_price = int(self.nutrition_price_input.text)
            
            if grain_price != self.grain_price or nutrition_price != self.nutrition_price:
                self.info.save_new_prices(grain_price, nutrition_price)

            food_type = self.food_type_spinner.text
            date = self.selected_date
            if quantity and grain_price and date and nutrition_price and food_type and quantity != 0 and grain_price != 0 and nutrition_price != 0:
                item = {}
                price = 0
                if food_type == "Gabona":
                    food_type = "Grain"
                    price = 14 * grain_price * quantity
                elif food_type == "Táp":
                    food_type = "Nutrition"
                    price = 12 * nutrition_price * quantity

                item = {
                    "date": date,
                    "quantity": quantity,
                    "total_price": price,
                    "food_type": food_type
                }
                self.storage.add_item(self.storage.generate_short_id(), "feed_data", item)

            self.display_message("Sikeres művelet!", success=True)
            Clock.schedule_once(lambda dt: self.go_back(None), 1)

        except Exception as e:
            self.display_message(f"Hiba: {e}", success=False)

    def display_message(self, message, success=False):
        color = (0, 0.7, 0, 1) if success else (0.7, 0, 0, 1)

        if not hasattr(self, 'message_label'):
            self.message_label = Label(
                text="",
                size_hint=(1, None),
                height=50,
                color=color,
                halign="left",
                valign="middle"
            )
            self.children[0].children[0].add_widget(self.message_label, index=0)

        self.message_label.text = message
        self.message_label.color = color

    def go_back(self, instance):
        self.manager.current = 'main'
