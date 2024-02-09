from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen



class NavigationDrawerScreen(MDScreen):
    pass


class Client_services(MDScreen):
    def __init__(self, **kwargs):
        super(Client_services, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)

    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.on_back_button()
            return True
        return False

    def on_back_button(self):
        self.manager.pop()

    def logout(self):
        self.manager.push("login", "right")
        self.ids.nav_drawer.set_state("close")

    def home(self):
        self.ids.nav_drawer.set_state("close")

    def location_screen(self):
        self.manager.push("location")
