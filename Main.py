import re
from kivymd.uix.menu import MDDropdownMenu
# from kivyauth.google_auth import initialize_google,login_google,logout_google
from kivy.lang import Builder
from kivymd import app
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.core.text import LabelBase
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

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
        # Enhanced password validation
        is_valid_password, password_error_message = self.validate_password(password)
        if not email or not re.match(email_regex, email):
            self.show_validation_dialog("Invalid Email")
        elif not is_valid_password:
            self.show_validation_dialog(password_error_message)
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
            return False, "Password must contain both uppercase and lowercase letters"

        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain at least one special character"

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
            username = user[1]
            # self.update(login_email, username)
            self.screen = Builder.load_file("menu_profile.kv")
            screen = self.root.get_screen('menu_profile')
            screen.ids.username.text = username
            screen.ids.email.text = login_email
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
        # client_id = open("client_id.txt")
        # client_secret = open("client_secret.txt")
        # initialize_google(self.after_login(), self.error_listener, client_id.read(),client_secret.read())
        screen_manager = ScreenManager()

        screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("client_services.kv"))
        screen_manager.add_widget(Builder.load_file("menu_profile.kv"))
        screen_manager.add_widget(Builder.load_file("menu_notification.kv"))
        screen_manager.add_widget(Builder.load_file("menu_bookings.kv"))
        screen_manager.add_widget(Builder.load_file("menu_reports.kv"))
        screen_manager.add_widget(Builder.load_file("hospital_book.kv"))
        screen_manager.add_widget(Builder.load_file("service_provider.kv"))
        screen_manager.add_widget(Builder.load_file("service_register_form.kv"))


        return screen_manager
    # #google auth
    # def after_login(self):
    #     pass
    # def error_listener(self):
    #     pass
    # def login(self):
    #     login_google()

    #-------------------------service-provider-flow-------------
    menu = None
    def open_dropdown(self):
        self.screen_service = Builder.load_file('service_register_form.kv')
        screen_service = self.root.current_screen
        if not self.menu:
            # Dropdown items (Replace these with your city names)
            cities = ["Hospital Facility Manager",
                      "Ambulance Facility Manager",
                      "Gym Facility Manager", "Doctors",
                      "Ambulance Drivers"]
            items = [
                {
                    "viewclass": "MDDropDownItem",
                    "text": city,
                    "callback": self.select_city,
                } for city in cities
            ]
            self.menu = MDDropdownMenu(items=items, width_mult=3,max_height=100, pos_hint={'center_x': 0, 'center_y': 0.9})

        # Open the dropdown menu
        self.menu.caller = self.screen_service.ids.dropdown_field
        self.menu.open()

    def select_city(self, instance,instance_item):
        # Callback function when a city is selected
        selected_city = instance_item.text
        print(instance_item.text)
        self.root.ids.dropdown_field.text = selected_city
        self.menu.dismiss()


# Run the app
if __name__ == '__main__':
    LabelBase.register(name="MPoppins", fn_regular="Poppins/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Poppins/Poppins-Bold.ttf")
    LoginApp().run()
