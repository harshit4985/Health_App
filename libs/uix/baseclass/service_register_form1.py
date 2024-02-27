import re
import sqlite3

from kivymd.icon_definitions import md_icons
from kivymd.uix.screen import MDScreen
from kivy.properties import BooleanProperty
from kivy.clock import Clock

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Creating the hospital_table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organization_name TEXT,
        established_year TEXT,
        District TEXT,
        State TEXT,
        pincode TEXT,0
        address TEXT,
        capsules INT,
        doc1 BLOB,
        doc2 BLOB
    )
''')


class ServiceRegisterForm1(MDScreen):
    # name_valid = BooleanProperty(False)
    # email_valid = BooleanProperty(False)
    password_valid = BooleanProperty(False)
    # phoneno_valid = BooleanProperty(False)
    # address_valid = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.auto_validate, 0.5)

    def auto_validate(self, *args):
        # self.name_valid = bool(self.ids.service_provider_name.text and len(self.ids.service_provider_name.text) > 3)
        # self.email_valid = bool(self.ids.service_provider_email.text and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',
        #                                                                           self.ids.service_provider_email.text))
        self.password_valid = bool(
            self.ids.service_provider_password.text and self.validate_password(self.ids.service_provider_password.text)[
                0])
        # self.phoneno_valid = bool(
        #     self.ids.service_provider_phoneno.text and len(self.ids.service_provider_phoneno.text) == 10)
        # self.address_valid = bool(
        #     self.ids.service_provider_address.text and len(self.ids.service_provider_address.text) > 3)
        # self.update_next_button()

    # def all_fields_valid(self):
    #     return all([self.name_valid, self.email_valid, self.password_valid, self.phoneno_valid, self.address_valid])

    # def update_next_button(self):
    #     self.ids.next_button.disabled = not self.all_fields_valid()

    # def on_name_change(self, instance, value):
    #     self.name_valid = bool(value and len(value) > 3)
    #     if not self.name_valid:
    #         self.ids.service_provider_name.error = True
    #         self.ids.service_provider_name.helper_text = 'Enter proper name.'
    #     else:
    #         self.ids.service_provider_name.error = False
    #         self.ids.service_provider_name.helper_text = ''
    #     # self.update_next_button()
    #
    # def on_email_change(self, instance, value):
    #     self.email_valid = bool(value and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value))
    #     if not self.email_valid:
    #         self.ids.service_provider_email.error = True
    #         self.ids.service_provider_email.helper_text = "Invalid email format."
    #     else:
    #         self.ids.service_provider_email.error = False
    #         self.ids.service_provider_email.helper_text = ""
    #     # self.update_next_button()
    #
    def on_password_change(self, instance, value):
        self.password_valid, hint_text = self.validate_password(value)
        if not self.password_valid:
            self.ids.service_provider_password.error = True
            self.ids.service_provider_password.helper_text = hint_text
        else:
            self.ids.service_provider_password.error = False
            self.ids.service_provider_password.helper_text = ""
    #     # self.update_next_button()
    #
    # def on_phoneno_change(self, instance, value):
    #     self.phoneno_valid = bool(value and len(value) == 10)
    #     if not self.phoneno_valid:
    #         self.ids.service_provider_phoneno.error = True
    #         self.ids.service_provider_phoneno.helper_text = "Invalid phone number (10 digits required)."
    #     else:
    #         self.ids.service_provider_phoneno.error = False
    #         self.ids.service_provider_phoneno.helper_text = ''
    #
    #     # self.update_next_button()
    #
    # def on_address_change(self, instance, value):
    #     stripped_value = value.strip() if value else ""
    #     self.address_valid = len(stripped_value) > 3
    #     if not self.address_valid:
    #         self.ids.service_provider_address.error = True
    #         self.ids.service_provider_address.helper_text = 'Enter a proper address.'
    #     else:
    #         self.ids.service_provider_address.error = False
    #         self.ids.service_provider_address.helper_text = ''
        # self.update_next_button()

    # def on_pre_enter(self, *args):
    #     self.reset_fields()

    def reset_fields(self):
        self.manager.push_replacement("signup", "right")
        self.ids.service_provider_name.text = ""
        self.ids.service_provider_name.error = False
        self.ids.service_provider_name.helper_text = ''

        self.ids.service_provider_email.text = ""
        self.ids.service_provider_email.error = False
        self.ids.service_provider_email.helper_text = ''

        self.ids.service_provider_password.text = ""
        self.ids.service_provider_password.error = False
        self.ids.service_provider_password.helper_text = ''

        self.ids.service_provider_phoneno.text = ""
        self.ids.service_provider_phoneno.error = False
        self.ids.service_provider_phoneno.helper_text = ''

        self.ids.service_provider_address.text = ""
        self.ids.service_provider_address.error = False
        self.ids.service_provider_address.helper_text = ''

    def register_validation(self):
        service_provider_name = self.ids.service_provider_name.text
        service_provider_email = self.ids.service_provider_email.text
        service_provider_password = self.ids.service_provider_password.text
        service_provider_phoneno = self.ids.service_provider_phoneno.text
        service_provider_address = self.ids.service_provider_address.text

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

        else:
            self.manager.push("service_register_form2")


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
