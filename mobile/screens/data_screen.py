from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from data.storage import Storage
from data.info import Information
import requests
import json

class DataScreen(Screen):
    def __init__(self, storage, counter, **kwargs):
        super().__init__(**kwargs)
        self.storage: Storage = storage
        self.counter: Information = counter
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        label = Label(
            text="DATA",
            size_hint=(1, None),
            height=50,
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
        )
        self.layout.add_widget(label)
        
        self.scrollview = ScrollView(size_hint=(1, 1))
    
        self.grid = GridLayout(cols=2, padding=10, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.scrollview.add_widget(self.grid)
        self.layout.add_widget(self.scrollview)
        
        send_button = Button(text="Küldés a szerverre", on_press=self.send_data)
        self.layout.add_widget(send_button)
        
        button = Button(text="Vissza", font_size=24, size_hint=(1, None), height=80)
        button.bind(on_press=self.go_to_main_page)
        self.layout.add_widget(button)

        self.add_widget(self.layout)

    def populate_data(self):
        # Clear the grid first
        self.grid.clear_widgets()

        # Access the data from JsonStore
        data = self.storage.data
        data_dict = {}

        # Build a dictionary from JsonStore
        for key in data.keys():
            data_dict[key] = data.get(key)

        # Populate the grid with the updated data
        for date, details in data_dict.items():
            self.grid.add_widget(Label(text=date, bold=True, color=(0, 0, 0, 1), size_hint_y=None, height=80))

            if isinstance(details, dict):
                detail_text = "\n".join([f"{k}: {v}" for k, v in details.items()])
            else:
                detail_text = str(details)

            self.grid.add_widget(Label(text=detail_text, color=(0, 0, 0, 1), size_hint_y=None, height=80))

    def send_data(self, instance):
        # Define your API endpoint
        upload_stock_url = "http://localhost:8000/dashboard/upload_stock"
        upload_data_url = "http://localhost:8000/dashboard/upload_data"
        
        stock = self.counter.info._data
        try:
            response = requests.post(upload_stock_url, data=json.dumps(stock), headers={'Content-Type': 'application/json'})
            
            # Check if the request was successful
            if response.status_code == 201:
                print("Stock sent successfully!")
            else:
                print(f"Failed to send stock. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending stock: {e}")
        
        
        data = self.storage.data._data
        print(data)
        # Send POST request
        try:
            response = requests.post(upload_data_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            
            # Check if the request was successful
            if response.status_code == 201:
                print("Data sent successfully!")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")
    
    def go_to_main_page(self, instance):
        self.manager.current = 'main'

    # This will be triggered every time the screen is entered
    def on_enter(self):
        self.populate_data()
