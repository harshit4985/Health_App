from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen



class NavigationDrawerScreen(MDScreen):
    pass


class Client_services(MDScreen):
    def logout(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'login'
        self.ids.nav_drawer.set_state("close")

    def home(self):
        self.ids.nav_drawer.set_state("close")

    def location_screen(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'left'
        app.root.current = 'location'
