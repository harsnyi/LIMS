from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from data.storage import Storage
from data.info import Information
from datetime import datetime
from kivy.clock import Clock

class SaleScreen(Screen):
    def __init__(self, storage, info, **kwargs):
        super().__init__(**kwargs)
        self.storage: Storage = storage
        self.info: Information = info
        self.selected_date = datetime.today().strftime("%Y-%m-%d")
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))


        label = Label(
            text="Sale Screen",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(label)
        
        label = Label(
            text="Hány darab került eladásra",
            size_hint=(1, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            
        )
        layout.add_widget(label)
        
        self.count_input = TextInput(
            input_filter='int',
            multiline=False,
            size_hint=(1, None),
            height=100
        )
        layout.add_widget(self.count_input)
        
        label = Label(
            text="Ide írd be az összeget",
            size_hint=(1, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
        )
        layout.add_widget(label)
        
        self.price_input = TextInput(
            input_filter='int',
            multiline=False,
            size_hint=(1, None),
            height=100
        )
        layout.add_widget(self.price_input)
        
        label = Label(
            text="Hány kilogram került eladásra?",
            size_hint=(1, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
        )
        layout.add_widget(label)
        
        self.kilo_input = TextInput(
            input_filter='float',
            multiline=False,
            size_hint=(1, None),
            height=100
        )
        layout.add_widget(self.kilo_input)
        
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
        save_button.bind(on_press=self.save_sale)
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
        # Switch back to the Main Page
        self.manager.current = 'main'
        
    def save_sale(self, instance):
        try:
            quantity = int(self.count_input.text)
            price = int(self.price_input.text)
            kilogram = float(self.kilo_input.text)
            date = self.selected_date
            if quantity and price and date and kilogram and quantity != 0 and kilogram != 0 and price != 0:
                
                self.counter.check_stock(quantity)
                item = {}
                if self.storage.already_exists(date, "sales"):
                    new_quantity = int(self.storage.data[date]["data"]["sales"]["quantity"]) + quantity
                    new_price = int(self.storage.data[date]["data"]["sales"]["price"]) + price
                    new_kilo = int(self.storage.data[date]["data"]["sales"]["kilogram"]) + kilogram
                    
                    item = {"quantity":new_quantity, "price":new_price, "kilogram": new_kilo}
                else:
                    item = {"quantity":quantity, "price":price, "kilogram": kilogram}
                    
                self.storage.add_item(date, "sales", item)
                self.info.modify_stock(-1 * quantity)
                
                self.display_message("Eladás sikeresen mentve!", success=True)
                Clock.schedule_once(lambda dt: self.go_to_main_page(None), 1)
                
        except Exception as e:
            print(f"Hiba adódott a mentéskor: {e}")
            self.display_message(f"Hiba: {str(e)}", success=False)
    
    def display_message(self, message, success=False):
        color = (0, 0.7, 0, 1) if success else (0.7, 0, 0, 1)

        if not hasattr(self, 'message_label'):
            self.message_label = Label(
                text="",
                size_hint=(1, None),
                height=50,
                color=color,
                halign="left",
                valign="middle",
            )
            self.children[0].children[0].add_widget(self.message_label, index=0)

        self.message_label.text = message
        self.message_label.color = color