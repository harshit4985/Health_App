from kivy import args
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty

from form_validation import BaseRegistrationScreen


class HospitalService(BaseRegistrationScreen):
    
    def validate_content(self):
        super().validate_content('oxiclinic')