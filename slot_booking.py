import sqlite3
from datetime import datetime
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen

# Create the BookSlot table if it doesn't exist

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS BookSlot (
        slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        book_date TEXT NOT NULL,
        book_time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()


# Builder.load_file("slot_booking.kv")


class S_button(MDRaisedButton):
    pass


class S_layout(BoxLayout):
    pass


class S_label(MDLabel):
    pass


class Slot_Booking(MDScreen):
    time_slots = ['9am - 11am', '11am - 1pm', '1pm - 3pm', '3pm - 5pm', '5pm - 7pm', '7pm - 9pm']

    def __init__(self, **kwargs):
        super(Slot_Booking, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)

    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.on_back_button()
            return True
        return False

    def on_back_button(self):
        self.manager.push_replacement("hospital_booking","right")

    def slot_booking_back_button(self, instance):
        self.manager.push_replacement("hospital_booking","right")
        self.ids.date_choosed.text = "Choose a date"
        for slots in Slot_Booking.time_slots:
            self.ids[slots].disabled = False
            self.ids[slots].md_bg_color = (1, 1, 1, 1)
        if hasattr(self, 'session_time'):
            delattr(self, 'session_time')
        print("Back To Hospital Page")

    def select_timings(self, button, label_text):
        self.session_time = label_text
        print(self.session_time)
        selected_slot = label_text
        for slot in Slot_Booking.time_slots:
            if slot == selected_slot:
                self.ids[slot].md_bg_color = (1, 1, 1, 1)
            else:
                self.ids[slot].md_bg_color = (1, 0, 0, 1)

    def slot_date_picker(self):
        current_date = datetime.now().date()
        date_dialog = MDDatePicker(year=current_date.year, month=current_date.month, day=current_date.day,
                                   size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.slot_save, on_cancel=self.slot_cancel)
        date_dialog.open()

    def slot_save(self, instance, value, date_range):
        # the date string in "year-month-day" format
        date_object = datetime.strptime(str(value), "%Y-%m-%d")
        # Format the date as "day-month-year"
        formatted_date = date_object.strftime("%d-%m-%Y")
        book_slot = app_tables.book_slot.search(book_date=formatted_date)
        book_times = [row['book_time'] for row in book_slot]
        print(formatted_date, book_times)
        for slots in Slot_Booking.time_slots:
            self.ids[slots].disabled = False
            if not book_times:
                print(book_times)
                for slots in Slot_Booking.time_slots:
                    self.ids[slots].disabled = False
            elif book_times:
                for slots in book_times:
                    self.ids[slots].disabled = True
            else:
                pass
        self.ids.date_choosed.text = formatted_date

    def slot_cancel(self, instance, value):
        print("cancel")

    def pay_now(self, instance, *args):
        session_date = self.ids.date_choosed.text
        # Extract the username from menu_profile
        screen = self.manager.get_screen('client_services')
        username = screen.ids.username.text
        if len(session_date) == 10 and hasattr(self, 'session_time') and self.session_time:
            print(username, session_date, self.session_time)
            self.manager.load_screen("payment_page")
            current_screen = self.manager.get_screen('payment_page')
            current_screen.ids.user_name.text = username
            current_screen.ids.session_date.text = session_date
            current_screen.ids.session_time.text = self.session_time
            self.manager.push("payment_page")
        elif len(session_date) == 13 and hasattr(self, 'session_time') and self.session_time:
            self.show_validation_dialog("Select Date")
        elif hasattr(self, 'session_time') == False and len(session_date) == 10:
            self.show_validation_dialog("Select Time")
        else:
            self.show_validation_dialog("Select Date and Time")

    def show_validation_dialog(self, message):
        # Create the dialog asynchronously
        Clock.schedule_once(lambda dt: self._create_dialog(message), 0)

    def _create_dialog(self, message):
        dialog = MDDialog(
            text=f"{message}",
            elevation=0,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()
