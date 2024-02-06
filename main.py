import anvil
from anvil import Timer
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog

from ServiceProviderMainPage import ServiceProviderMain, ServiceProfile, ServiceNotification, ServiceSlotAdding, \
    ServiceSupport
from kivymd.uix.screen import MDScreen

from signup_login import Signup, Login, Forgot_password
from ServiceRegister import ServiceRegisterForm, HospitalContent, MobileCareContent, GymContent, \
    RegisterPage2, HospitalListTable
from slot_booking import Slot_Booking
from support_page import Support_page
from fetch_pincode_page import Location
from payment_page import Payment
from client_services import Client_services, Profile, Booking, Notification, Report

# from kivyauth.google_auth import initialize_google,login_google,logout_google
from kivy.graphics import Mesh, Color
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.core.text import LabelBase
from kivymd.uix.behaviors import FakeRectangularElevationBehavior, CommonElevationBehavior

# from kivy.uix.webview import WebView
# from google_auth_oauthlib.flow import InstalledAppFlow
# import webbrowser
# from google.auth.credentials import Credentials

import razorpay
# from crosswalk import WebView
import sqlite3
from kivymd.uix.floatlayout import MDFloatLayout

Window.size = (320, 580)

# SQLite database setup
conn = sqlite3.connect("users.db")
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
# Create the BookSlot table if it doesn't exist

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

class ProfileCard(MDFloatLayout, CommonElevationBehavior):
    pass


class NavigationDrawerScreen(MDScreen):
    pass


class LoginApp(MDApp):

    def build(self):
        self.icon = "images/shot.png"
        self.theme_cls.theme_style = "Light"
        self.check_internet_status_timer = Timer(interval=5000, repeating=True, enabled=True,
                                                 tick=self.check_internet_status)
        screen_manager = ScreenManager()
        screen_widgets = [
            # Builder.load_file("main_sc.kv"),
            # Login("login"),
            # Signup("signup"),
            # Forgot_password("forgot_password"),
            # Client_services("client_services"),
            # Location("client_services1"),
            # Profile("menu_profile"),
            # Notification("menu_notification"),
            # Booking("menu_bookings"),
            # Report("menu_reports"),
            # Support_page("menu_support"),
            # Builder.load_file("hospital_book.kv"),
            # Slot_Booking(name="slot_booking"),
            # Payment("payment_page.kv"),
            # ServiceProviderMain(name="service_provider_main_page"),
            # ServiceProfile(name="service_profile"),
            # ServiceNotification(name="service_notification"),
            # ServiceSlotAdding(name="service_slot_adding"),
            # ServiceSupport(name="service_support"),
            # Slot_Booking("slot_booking"),
            # Payment("payment_page"),
            ServiceRegisterForm(),
            HospitalContent(),
            MobileCareContent(),
            GymContent(),
            RegisterPage2(),
            HospitalListTable()
        ]
        for widget in screen_widgets:
            screen_manager.add_widget(widget)

        return screen_manager

    def check_internet_status(self, **event_args):
        try:
            anvil.server.call('check_internet_status')
            # If the check is successful, update UI or enable features as needed
        except anvil.server.AnvilWrappedError as e:
            self.handle_network_error(e)

    def handle_network_error(self, e):
        # Handle specific errors and display appropriate messages to the user
        self.show_validation_dialog("Network Error: Please check your internet connection.")

    def show_validation_dialog(self, message):
        # Create the dialog asynchronously
        Clock.schedule_once(lambda dt: self._create_dialog(message), 0)

    def _create_dialog(self, message):
        dialog = MDDialog(
            text=f"{message}",
            elevation=0,
        )
        dialog.open()

    def client_services1(self):
        self.root.transition = SlideTransition(direction='left')
        self.root.current = 'client_services1'

    def registration_submit(self):
        self.screen = Builder.load_file("service_register_form.kv")
        screen = self.root.current_screen
        username = screen.ids.name.text
        print(username)

    # hospital_Book page logic
    def back_button_hospital_book(self):
        self.root.transition = SlideTransition(direction='right')
        self.root.current = 'client_services'

    # # logic for back button in payment_page
    def payment_page_backButton(self):
        # Extract the username from menu_profile
        self.screen = Builder.load_file("menu_profile.kv")
        screen = self.root.get_screen('menu_profile')
        username = screen.ids.username.text
        print(username)
        # Execute the SQL DELETE statement
        cursor.execute("DELETE FROM BookSlot WHERE username = ?", (username,))
        # Commit the changes and close the connection
        conn.commit()
        self.root.transition = SlideTransition(direction='right')
        self.root.current = 'slot_booking'


# Run the app
if __name__ == '__main__':
    LabelBase.register(name="Broboto", fn_regular="roboto/Roboto-Bold.ttf")

    app = LoginApp()
    Window.bind(on_request_close=app.stop)
    app.run()
