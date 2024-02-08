from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class Notification(MDScreen):
    def notification_back(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'client_services'
        screen = app.root.get_screen('client_services')
        screen.ids.nav_drawer.set_state("close")
