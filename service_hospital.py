import sqlite3
from kivymd.uix.screen import MDScreen
from form_validation import BaseRegistrationScreen


class HospitalService(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super(HospitalService, self).__init__(**kwargs)

    def validate_content(self):
        return super().validate_content()
