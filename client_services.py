from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

Builder.load_file("client_services.kv")
Builder.load_file("menu_profile.kv")
Builder.load_file("menu_notification.kv")
Builder.load_file("menu_bookings.kv")
Builder.load_file("menu_reports.kv")

class Client_services(MDScreen):
    def logout(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'login'
        self.ids.nav_drawer.set_state("close")
    def home(self):
        self.ids.nav_drawer.set_state("close")

class Profile(MDScreen):
    def profile_back(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'client_services'
        screen = app.root.get_screen('client_services')
        screen.ids.nav_drawer.set_state("close")

class Booking(MDScreen):
    def booking_back(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'client_services'
        screen = app.root.get_screen('client_services')
        screen.ids.nav_drawer.set_state("close")

class Notification(MDScreen):
    def notification_back(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'client_services'
        screen = app.root.get_screen('client_services')
        screen.ids.nav_drawer.set_state("close")

class Report(MDScreen):
    def reports_back(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'client_services'
        screen = app.root.get_screen('client_services')
        screen.ids.nav_drawer.set_state("close")