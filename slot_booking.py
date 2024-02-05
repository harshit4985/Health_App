import cProfile
from datetime import datetime
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen

Builder.load_file("slot_booking.kv")


class Slot_Booking(MDScreen):
    time_slots = ['9am - 11am', '11am - 1pm', '1pm - 3pm', '3pm - 5pm', '5pm - 7pm', '7pm - 9pm']

    def slot_booking_back_button(self, instance):
        app = MDApp.get_running_app()
        app.root.transition = SlideTransition(direction='right')
        app.root.current = 'hospital_book'
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

    DATE_PICKER_SIZE = (150, 150)

    def slot_date_picker(self):
        date_dialog = MDDatePicker(
            year=datetime.now().date().year,
            month=datetime.now().date().month,
            day=datetime.now().date().day,
            size_hint=(None, None),
            size=self.DATE_PICKER_SIZE
        )
        date_dialog.bind(on_save=self.on_date_save, on_cancel=self.on_date_cancel)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        # Handle save event here
        pass

    def on_date_cancel(self, instance, value):
        # Handle cancel event here
        pass

    # date_picker_initialized = False
    # def initialize_date_picker(self, dt):
    #     if not self.date_picker_initialized:
    #         current_date = datetime.now().date()
    #         self.date_dialog = MDDatePicker(
    #             year=current_date.year,
    #             month=current_date.month,
    #             day=current_date.day,
    #             size_hint=(None, None),
    #             size=(150, 150)
    #         )
    #         self.date_dialog.bind(on_save=self.slot_save, on_cancel=self.slot_cancel)
    #         self.date_picker_initialized = True
    #
    # def slot_date_picker(self):
    #     # Schedule the initialization of the date picker with a slight delay
    #     Clock.schedule_once(self.initialize_date_picker, 0.1)
    #     # Open the date picker
    #     Clock.schedule_once(lambda dt: self.date_dialog.open(), 0.2)

    def pay_now(self, instance, *args):
        session_date = self.ids.date_choosed.text
        # Extract the username from menu_profile
        app = MDApp.get_running_app()
        screen = app.root.get_screen('client_services')
        username = screen.ids.username.text
        if len(session_date) == 10 and hasattr(self, 'session_time') and self.session_time:
            print(username, session_date, self.session_time)
            current_screen = app.root.get_screen('payment_page')
            current_screen.ids.user_name.text = username
            current_screen.ids.session_date.text = session_date
            current_screen.ids.session_time.text = self.session_time
            app.root.transition.direction = 'left'
            app.root.current = 'payment_page'
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
