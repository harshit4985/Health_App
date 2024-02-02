import anvil
from anvil import Timer
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner

from ServiceProviderMainPage import ServiceProviderMain, ServiceProfile, ServiceNotification, ServiceSlotAdding, \
    ServiceSupport
from kivymd.uix.screen import MDScreen

from signup_login import Signup, Login, Forgot_password
from ServiceProvider import ServiceRegisterForm
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
from kivymd.uix.behaviors import FakeRectangularElevationBehavior

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
class OpenGLScreen(Screen):
    def __init__(self, **kwargs):
        super(OpenGLScreen, self).__init__(**kwargs)
        self.opengl_widget = OpenGLWidget()
        self.add_widget(self.opengl_widget)

class OpenGLWidget(Widget):
    def __init__(self, **kwargs):
        super(OpenGLWidget, self).__init__(**kwargs)
        self.vertices = []
        self.indices = []
        self.angle = 0
        self.create_square()

    def create_square(self):
        # Define square vertices
        self.vertices = [
            -50, -50, 0, 1, 0, 0, 1,  # Vertex 1 (x, y, z, r, g, b, a)
            50, -50, 0, 0, 1, 0, 1,   # Vertex 2
            50, 50, 0, 0, 0, 1, 1,    # Vertex 3
            -50, 50, 0, 1, 1, 0, 1    # Vertex 4
        ]
        # Define square indices
        self.indices = [0, 1, 2, 2, 3, 0]

    def on_size(self, instance, value):
        self.create_square()
    def on_touch_down(self, touch):
        pass
    def on_touch_move(self, touch):
        pass
    def on_touch_up(self, touch):
        pass
    def update(self, dt):
        # Rotate the square
        self.angle += 1
        self.angle %= 360
    def draw(self):
        with self.canvas:
            Color(1, 1, 1, 1)
            Mesh(vertices=self.vertices, indices=self.indices, mode='triangles')

class ProfileCard(MDFloatLayout, FakeRectangularElevationBehavior):
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
        screen_manager.add_widget(Builder.load_file("main_sc.kv"))
        screen_manager.add_widget(Login("login"))
        screen_manager.add_widget(Signup("signup"))
        screen_manager.add_widget(Forgot_password("forgot_password"))
        screen_manager.add_widget(Client_services("client_services"))
        screen_manager.add_widget(Location("client_services1"))
        screen_manager.add_widget(Profile("menu_profile"))
        screen_manager.add_widget(Notification("menu_notification"))
        screen_manager.add_widget(Booking("menu_bookings"))
        screen_manager.add_widget(Report("menu_reports"))
        screen_manager.add_widget(Support_page("menu_support"))
        screen_manager.add_widget(Builder.load_file("hospital_book.kv"))
        screen_manager.add_widget(Slot_Booking(name="slot_booking"))
        screen_manager.add_widget(Payment("payment_page.kv"))
        screen_manager.add_widget(ServiceProviderMain(name="service_provider_main_page"))
        screen_manager.add_widget(ServiceProfile(name="service_profile"))
        screen_manager.add_widget(ServiceNotification(name="service_notification"))
        screen_manager.add_widget(ServiceSlotAdding(name="service_slot_adding"))
        screen_manager.add_widget(ServiceSupport(name="service_support"))
        screen_manager.add_widget(Slot_Booking("slot_booking"))
        screen_manager.add_widget(Payment("payment_page"))
        # screen_manager.add_widget(ServiceProviderMain(name="service_provider_main_page"))
        # screen_manager.add_widget(ServiceProfile(name="service_profile"))
        # screen_manager.add_widget(ServiceNotification(name="service_notification"))
        # screen_manager.add_widget(ServiceSlotAdding(name="service_slot_adding"))
        # screen_manager.add_widget(ServiceSupport(name="service_support"))
        screen_manager.add_widget(ServiceRegisterForm())
        # Create the OpenGL screen and add it to the ScreenManager
        opengl_screen = OpenGLScreen(name="opengl_screen")
        screen_manager.add_widget(opengl_screen)

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