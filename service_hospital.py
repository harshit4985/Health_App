from kivy import args
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty

from form_validation import BaseRegistrationScreen


class HospitalService(BaseRegistrationScreen):
    extra_info = BooleanProperty(False)
    extra_info2 = BooleanProperty(False)
    District = BooleanProperty(False)
    State = BooleanProperty(False)
    pincode = BooleanProperty(False)
    address = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.auto_validate, 0.5)

    def auto_validate(self, *args):
        self.extra_info = bool(self.ids.extra_info.text and len(self.ids.extra_info.text) > 3)
        self.extra_info2 = bool(self.ids.extra_info2.text)  # Assuming extra_info2 should not be empty
        self.District = bool(self.ids.District.text)
        self.State = bool(self.ids.State.text)
        self.pincode = bool(
            self.ids.pincode.text and len(self.ids.pincode.text) == 6)  # Assuming pincode should be exactly 6 digits
        self.address = bool(self.ids.address.text and len(self.ids.address.text) > 3)
        self.update_next_button()

    def all_fields_valid(self):
        return all([self.extra_info, self.extra_info2, self.District, self.State, self.pincode, self.address])

    def update_next_button(self):
        self.ids.next_button.disabled = not self.all_fields_valid()

    def register_validation(self):
        if self.all_fields_valid():
            # Perform registration process
            pass
        else:
            # Handle invalid fields
            pass

    def on_organization_change(self, instance, value):
        self.extra_info = bool(value and len(value) > 3)
        if not self.extra_info:
            self.ids.extra_info.error = True
            self.ids.extra_info.helper_text = 'Enter proper name.'
        else:
            self.ids.extra_info.error = False
            self.ids.extra_info.helper_text = ''
        self.update_next_button()

    def on_year_change(self, instance, value):
        self.extra_info2 = bool(value)
        if not self.extra_info2:
            self.ids.extra_info2.error = True
            self.ids.extra_info2.helper_text = "Invalid year."
        else:
            self.ids.extra_info2.error = False
            self.ids.extra_info2.helper_text = ''
        self.update_next_button()

    def on_district_change(self, instance, value):
        self.District = bool(value)
        if not self.District:
            self.ids.District.error = True
            self.ids.District.helper_text = 'Enter proper district.'
        else:
            self.ids.District.error = False
            self.ids.District.helper_text = ''
        self.update_next_button()

    def on_state_change(self, instance, value):
        self.State = bool(value)
        if not self.State:
            self.ids.State.error = True
            self.ids.State.helper_text = "Enter proper state."
        else:
            self.ids.State.error = False
            self.ids.State.helper_text = ''
        self.update_next_button()

    def on_pincode_change(self, instance, value):
        self.pincode = bool(value and len(value) == 6)
        if not self.pincode:
            self.ids.pincode.error = True
            self.ids.pincode.helper_text = 'Enter a valid 6-digit pincode.'
        else:
            self.ids.pincode.error = False
            self.ids.pincode.helper_text = ''
        self.update_next_button()

    def on_address_change(self, instance, value):
        self.address = bool(value and len(value) > 3)
        if not self.address:
            self.ids.address.error = True
            self.ids.address.helper_text = 'Enter a proper address.'
        else:
            self.ids.address.error = False
            self.ids.address.helper_text = ''
        self.update_next_button()
