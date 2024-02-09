from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen



class BookingInfo(MDScreen):
    # hospital_Book page logic
    def back_button_hospital_book(self):
        self.manager.push("client_services")
