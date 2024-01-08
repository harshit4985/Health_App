import re
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from ServiceProvider import ServiceRegister,ServiceProvider

from kivy.lang import Builder
from kivymd import app
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.core.text import LabelBase
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from datetime import datetime


import sqlite3
from kivymd.uix.floatlayout import MDFloatLayout


Window.size = (310, 580)

# SQLite database setup
conn = sqlite3.connect("users.db")  # Replace "users.db" with your desired database name
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL,
        pincode TEXT NOT NULL
    )
''')

conn.commit()



class ProfileCard(MDFloatLayout, FakeRectangularElevationBehavior):
    pass

# Create the main app class
class LoginApp(MDApp):


    def validate_inputs(self, instance, *args):
        self.screen=Builder.load_file("signup.kv")
        screen = self.root.current_screen
        username = screen.ids.signup_username.text
        email = screen.ids.signup_email.text
        password = screen.ids.signup_password.text
        phone = screen.ids.signup_phone.text
        pincode = screen.ids.signup_pincode.text
        print(username)
        print(email)
        print(password)
        print(phone)
        print(pincode)

        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not email or not re.match(email_regex, email):
            self.show_validation_dialog("Invalid Email")
        elif not password or len(password) < 6:
            self.show_validation_dialog("Invalid Password (at least 6 characters)")
        elif not pincode or len(pincode) != 6:
            self.show_validation_dialog("Invalid Pincode (6 digits required)")
        elif not phone or len(phone) != 10:
            self.show_validation_dialog("Invalid Phone number (10 digits required)")
        else:
            #If validation is successful, insert into the database
            cursor.execute('''
                        INSERT INTO users (username, email, password, phone, pincode)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (username, email, password, phone, pincode))
            conn.commit()
            # Navigate to the success screen
            self.root.transition = SlideTransition(direction='left')
            self.root.current = 'login'
 

    #password validation
    def validate_password(self, password):
        # Check if the password is not empty
        if not password:
            return False, "Password cannot be empty"

        # Check if the password has at least 8 characters
        if len(password) < 6:
            return False, "Password must have at least 6 characters"

        # Check if the password contains both uppercase and lowercase letters
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain uppercase, lowercase"

        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain a special character"

        # All checks passed; the password is valid
        return True, "Password is valid"

    def login_page(self,  instance, *args):
        self.screen = Builder.load_file("login.kv")
        screen1 = self.root.current_screen
        login_email = screen1.ids.login_email.text
        login_password = screen1.ids.login_password.text
        # Check if the user exists in the database for login
        cursor.execute('''
            SELECT * FROM users
            WHERE email = ? AND password = ?
        ''', (login_email, login_password))
        user = cursor.fetchone()

        if user:
            # Login successful
            print("Login successful. User details:", user)
            self.root.transition.direction = 'left'
            self.root.current = 'client_services'
        else:
            # Login failed
            self.show_validation_dialog("Invalid email or password")

    def show_validation_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

    def build(self):

        screen_manager = ScreenManager()

        screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("client_services.kv"))
        screen_manager.add_widget(Builder.load_file("menu_profile.kv"))
        screen_manager.add_widget(Builder.load_file("menu_notification.kv"))
        screen_manager.add_widget(Builder.load_file("menu_bookings.kv"))
        screen_manager.add_widget(Builder.load_file("menu_reports.kv"))
        screen_manager.add_widget(Builder.load_file("menu_support.kv"))
        screen_manager.add_widget(Builder.load_file("hospital_book.kv"))
        screen_manager.add_widget(ServiceProvider("service_provider"))
        screen_manager.add_widget(ServiceRegister("service_register_form"))
        screen_manager.add_widget(Builder.load_file("slot_booking.kv")
        screen_manager.add_widget(Builder.load_file("payment_page.kv"))

        return screen_manager


    #-------------------------service-provider-flow-------------
    menu = None
    def open_dropdown(self):
        self.screen_service = Builder.load_file('service_register_form.kv')
        screen_service = self.root.current_screen
        if not self.menu:
            # Dropdown items (Replace these with your city names)
            cities = ["India",
                      "America",
                      "Russia",
                      "China"]
            items = [
                {
                    "viewclass": "MDDropDownItem",
                    "text": city,
                    "callback": self.select_city,
                } for city in cities
            ]
            self.menu = MDDropdownMenu(items=items, width_mult=3,max_height=300, pos_hint={'center_x': 0.5, 'center_y': 3})

        # Open the dropdown menu
        self.menu.caller = self.screen_service.ids.dropdown_nation
        self.menu.open()

    def select_city(self, instance,instance_item):
        # Callback function when a city is selected
        selected_city = instance_item.text
        print(instance)
        # self.root.ids.dropdown_nation.text = selected_city
        # self.menu.dismiss()

    def on_save(self, instance, value, date_range):
        print(value)
        print(date_range)
        self.screen = Builder.load_file("hospital_book.kv")
        screen_hos = self.root.current_screen
        screen_hos.ids.dummy_widget.text = str(value)
        #self.show_date_dialog(value)

    # click Cancel
    def on_cancel(self, instance, value):
        print("cancel")
        self.screen = Builder.load_file("service_register_form.kv")
        screen_hos_cancel = self.root.current_screen
        #screen_hos_cancel.ids.hospital_year.text = "You Clicked Cancel"

    def show_date_picker(self,arg):
        date_dialog = MDDatePicker( size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


    # hospital_Book page logic
    # functionality for back button in hospital book
    def back_button_hospital_book(self):
        self.root.transition = SlideTransition(direction='left')
        self.root.current = 'client_services'


    # Slot_Booking page logic
    def slot_save(self, instance, value, date_range):
        # the date string in "year-month-day" format
        # date_object = datetime.strptime(str(value), "%Y-%m-%d")
        # Format the date as "day-month-year"
        # formatted_date = date_object.strftime("%d-%m-%Y")
        self.screen = Builder.load_file("slot_booking.kv")
        screen = self.root.current_screen
        screen.ids.slot_date_label.text = str(value)
        screen.ids.session_date.text = str(value)

    def slot_cancel(self, instance, value):
        print("cancel")
        self.screen = Builder.load_file("slot_booking.kv")
        screen_hos_cancel = self.root.current_screen
        screen_hos_cancel.ids.slot_date_label.text = "You Clicked Cancel"
    def slot_date_picker(self):
        date_dialog = MDDatePicker(year=2024, month=1, day=4, size_hint=(None, None), size=(150, 150))
        date_dialog.bind(on_save=self.slot_save, on_cancel=self.slot_cancel)
        date_dialog.open()

    def checkbox_click(self, checkbox, value, time):
        if value:
            self.screen = Builder.load_file("slot_booking.kv")
            screen = self.root.current_screen
            screen.ids.session_time.text = str(time)

    def pay_now(self, instance, *args):
        self.screen1 = Builder.load_file("slot_booking.kv")
        screen1 = self.root.current_screen
        session_date = screen1.ids.session_date.text
        session_time = screen1.ids.session_time.text
        self.screen = Builder.load_file("menu_profile.kv")
        screen = self.root.get_screen('menu_profile')
        username = screen.ids.username.text
        print(username)


        # if len(session_date) == 10 and len(session_time) >= 9:
        #     # If date and time are successfully Selected, insert into the database
        #
        #     cursor.execute('''
        #            INSERT INTO BookSlot (user_id, username, book_date, book_time)
        #            VALUES (?, ?, ?, ?)
        #        ''', (user_id, username, session_date, session_time))

        #
        #     self.root.transition.direction = 'left'
        #     self.root.current = 'payment_page'
        # elif len(session_date) == 4 and len(session_time) >= 9 :
        #     self.show_validation_dialog("Select Date")
        # elif len(session_date) == 10 and len(session_time) == 4:
        #     self.show_validation_dialog("Select Time")
        # else:
        #     self.show_validation_dialog("Select Date and Time")





#------------------------menu-support-flow-------------------------

    def show_customer_support_dialog(self):
        dialog = MDDialog(
            title="Contact Customer Support",
            text="Call Customer Support at: +1-800-123-4567"
        )
        dialog.open()


    def show_doctor_dialog(self):
        dialog = MDDialog(
            title="Call On-Call Doctor",
            text="Call On-Call Doctor at: +1-888-765-4321"
        )
        dialog.open()


    def submit_ticket(self, issue_title, issue_description):
        # self.root.transition = SlideTransition(direction='right')
        # self.root.current = 'client_services'
        self.screen = Builder.load_file("menu_support.kv")
        screen = self.root.current_screen
        submitted_title = screen.ids.issue_title.text
        submitted_description = screen.ids.issue_description.text
        print(f"Submitted Issue Title: {submitted_title}")
        print(f"Submitted Issue Description: {submitted_description}")


    def show_ticket_popup(self):
        self.screen = Builder.load_file("menu_support.kv")
        screen = self.root.current_screen
        submitted_title = screen.ids.issue_title.text
        submitted_description = screen.ids.issue_description.text

        # Create and show the popup
        ticket_popup = MDDialog(
            title="Ticket Raised",
            text=f"Issue '{submitted_title}' has been raised.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    md_bg_color=(1, 0, 0, 1),
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    font_size=15,
                    on_release=lambda *args: ticket_popup.dismiss()
                ),
            ],
        )
        ticket_popup.open()
        screen.ids.issue_title.text = ""
        screen.ids.issue_description.text = ""

#------------------------menu-support-flow-------------------------



# Run the app
if __name__ == '__main__':
    LabelBase.register(name="MPoppins", fn_regular="Poppins/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Poppins/Poppins-Bold.ttf")
    LoginApp().run()
