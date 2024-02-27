from kivy.core.window import Window

from form_validation import BaseRegistrationScreen


class OxyGymServiceDoc(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super(OxyGymServiceDoc, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)

    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            super().doc_reset_field()
            return True
        return False

    def file_manager_open(self, field_id):
        super().file_manager_open(field_id)