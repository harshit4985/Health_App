from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen



class BookingInfo(MDScreen):
    # hospital_Book page logic
    def back_button_hospital_book(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = 'client_services'
