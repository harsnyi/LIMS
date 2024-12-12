from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivymd.uix.pickers import MDDatePicker
from data.storage import Storage
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from datetime import datetime

class OtherExpensesScreen(Screen):
    def __init__(self, storage, info, **kwargs):
        super().__init__(**kwargs)
        self.storage: Storage = storage
        self.selected_date = datetime.today().strftime("%Y-%m-%d")
        self.selected_expense = None

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        label = Label(
            text="Egyéb kiadás hozzáadása",
            size_hint=(1, None),
            height=50,
            color=(1, 1, 1, 1)
        )
        layout.add_widget(label)

        label = Label(
            text="Válassz egy típust",
            size_hint=(1, None),
            size=(100, 50),
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
        )
        layout.add_widget(label)

        self.spinner = Spinner(
            text="Egyéb kiadás",
            values=("vitamin", "gyógyszer", "premix", "szelidgesztenye por", "takarmányszén"),
            size_hint=(1, None),
            height=100,
        )
        self.spinner.bind(text=self.on_spinner_select)
        layout.add_widget(self.spinner)

        label = Label(
            text="Ide írd az összeget",
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
            text="Add meg a dátumot (mai dátum az alapértelmezett)",
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

        button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=180)

        back_button = Button(
            text="Vissza",
            font_size=24,
            size_hint=(1, None),
            height=180,
            background_color=(1, 0.75, 0.4, 1),
            color=(1, 1, 1, 1),
            background_normal='',
            background_down='',
        )
        back_button.bind(on_press=self.go_to_main_page)
        button_layout.add_widget(back_button)

        save_button = Button(
            text="Mentés",
            font_size=24,
            size_hint=(1, None),
            height=180,
            background_color=(0.54, 0.75, 0.64, 1),
            color=(1, 1, 1, 1),
            background_normal='',
            background_down='',
        )
        save_button.bind(on_press=self.save_other_expense)
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)

        self.add_widget(scroll_view)

    def on_spinner_select(self, spinner, text):
        self.selected_expense = text

    def show_date_picker(self, instance):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance, value, date_range):
        self.selected_date = value.strftime("%Y-%m-%d")
        self.date_button.text = self.selected_date

    def go_to_main_page(self, instance):
        self.manager.current = 'main'

    def save_other_expense(self, instance):
        # try:
            item = {}
            price = int(self.price_input.text)
            expense_type = self.selected_expense
            date = self.selected_date
            if expense_type and price and date:
                if self.storage.already_exists(date, "saled_eggs"):
                    pass
                item = {"price":price, "expense_type":expense_type}
                self.storage.add_item(date, "other_expenses", item)
                self.display_message("Egyéb kiadás sikeresen mentve!", success=True)
                Clock.schedule_once(lambda dt: self.go_to_main_page(None), 1)
            else:
                self.display_message("Valamelyik mező kitöltetlenül maradt!", success=False)
        # except Exception as e:
        #     print(f"Hiba adódott a mentéskor: {e}")
        #     self.display_message(f"Hiba: {str(e)}", success=False)

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
