import re

from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class HorizontalLineWidget(MDBoxLayout):
    pass


class ServiceRegisterForm2(MDScreen):
    def __init__(self, **kwargs):
        super(ServiceRegisterForm2, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)
    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.on_back_button()
            return True
        return False

    def on_back_button(self):
        self.manager.push_replacement("service_register_form1", "right")
    def register(self):
        print("registered")