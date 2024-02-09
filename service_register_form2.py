import re

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


class HorizontalLineWidget(MDBoxLayout):
    pass


class ServiceRegisterForm2(MDScreen):
    checkbox = None

    def __init__(self, **kwargs):
        super(ServiceRegisterForm2, self).__init__(**kwargs)

    def on_checkbox_active(self, checkbox, checkbox_value, add_branch_button):
        self.checkbox = checkbox
        if checkbox_value == 'Hospital':
            print(f"Selected service provider type: {checkbox_value}")
            add_branch_button.disabled = not checkbox.active
            if checkbox.active:
                self.ids.plus_icon_h.text_color = (1, 0, 0, 1)
                self.ids.add_text_h.text_color = (1, 0, 0, 1)
        elif checkbox_value == 'Mobile-Hospital':
            print(f"Selected service provider type: {checkbox_value}")
            add_branch_button.disabled = not checkbox.active
            if checkbox.active:
                self.ids.plus_icon_m_h.text_color = (1, 0, 0, 1)
                self.ids.add_text_m_h.text_color = (1, 0, 0, 1)
        elif checkbox_value == 'Oxi-Gym':
            print(f"Selected service provider type: {checkbox_value}")
            add_branch_button.disabled = not checkbox.active
            if checkbox.active:
                self.ids.plus_icon_o_g.text_color = (1, 0, 0, 1)
                self.ids.add_text_o_g.text_color = (1, 0, 0, 1)
        else:
            print(f"Selected service provider type : {checkbox_value} is inactive")

    def update_width(self, *args):
        if self.dialog:
            # Get the window width
            window_width = Window.width

            # Set the width of the dialog (you can adjust the multiplier as needed)
            self.dialog.width = window_width * 0.8

    def cancel_dialog(self, instance):
        print("CANCEL button clicked")
        self.dialog.dismiss()

    button = None

    def ok_dialog(self, content_cls, list_button):
        self.button = list_button
        print("OK button clicked")
        if content_cls.validate_content():
            print("successful")
            self.checkbox.disabled = True
            self.button.disabled = False
            self.ids.hint_label.text = ""
            self.dialog.dismiss()

    def register_validation(self):
        service_provider_name = self.ids.service_provider_name.text
        service_provider_email = self.ids.service_provider_email.text
        service_provider_password = self.ids.service_provider_password.text
        service_provider_phoneno = self.ids.service_provider_phoneno.text
        service_provider_address = self.ids.service_provider_address.text
        hospital_manager = self.ids.hospital_manager
        mobile_hospital_manager = self.ids.mobile_hospital_manager
        oxigym_manager = self.ids.oxigym_manager
        # Validation logic
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        is_valid_password, password_error_message = self.validate_password(service_provider_password)

        if not service_provider_name:
            self.ids.service_provider_name.error = True
            self.ids.service_provider_name.helper_text = "This field is required."
            self.ids.service_provider_name.required = True
        elif not service_provider_email or not re.match(email_regex, service_provider_email):
            self.ids.service_provider_email.error = True
            self.ids.service_provider_email.helper_text = "Invalid email format."
            self.ids.service_provider_email.required = True
        elif not is_valid_password:
            self.ids.service_provider_password.error = True
            self.ids.service_provider_password.helper_text = password_error_message
            self.ids.service_provider_password.required = True
        elif not service_provider_phoneno or len(service_provider_phoneno) != 10:
            self.ids.service_provider_phoneno.error = True
            self.ids.service_provider_phoneno.helper_text = "Invalid phone number (10 digits required)."
            self.ids.service_provider_phoneno.required = True
        elif not service_provider_address:
            self.ids.service_provider_address.error = True
            self.ids.service_provider_address.helper_text = "This field is required."
            self.ids.service_provider_address.required = True
        elif not (hospital_manager.active or mobile_hospital_manager.active or oxigym_manager.active):
            self.ids.hint_label.text = "Please select at least one checkbox"
        elif not (hospital_manager.disabled or mobile_hospital_manager.disabled or oxigym_manager.disabled):
            self.ids.hint_label.text = "Please add values"
        else:
            self.manager.push("login")
            self.ids.service_provider_name.text = ""
            self.ids.service_provider_email.text = ""
            self.ids.service_provider_password.text = ""
            self.ids.service_provider_phoneno.text = ""
            self.ids.service_provider_address.text = ''
            self.ids.hospital_manager.active = False
            self.ids.mobile_hospital_manager.active = False
            self.ids.oxigym_manager.active = False
            self.ids.hint_label.text = ""

    # password validation
    def validate_password(self, password):
        # Check if the password is not empty
        if not password:
            return False, "Password cannot be empty"

        # Check if the password has at least 8 characters
        if len(password) < 6:
            return False, "Password must have at least 6 characters"

        # Check if the password contains both uppercase and lowercase letters
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain uppercase, lowercase"

        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain a special character"

        # All checks passed; the password is valid
        return True, "Password is valid"
