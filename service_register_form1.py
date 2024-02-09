from kivy.core.window import Window
from kivymd.uix.screen import MDScreen


class ServiceRegisterForm1(MDScreen):
    def __init__(self, **kwargs):
        super(ServiceRegisterForm1, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)

    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.on_back_button()
            return True
        return False

    def on_back_button(self):
        self.manager.pop()