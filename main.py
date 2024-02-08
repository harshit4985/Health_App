from kivy import platform

import anvil
from anvil import Timer
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog

from service_provider_main_page import ServiceProviderMain, ServiceProfile, ServiceNotification, ServiceSlotAdding, ServiceSupport
from kivymd.uix.screen import MDScreen



from forgot_password import ForgotPassword
from menu_support import SupportPage
from menu_profile import Profile
from menu_bookings import Booking
from menu_reports import Report
from menu_notification import Notification

from ServiceRegister import ServiceRegisterForm, HospitalContent, MobileCareContent, GymContent, RegisterPage2, HospitalListTable
from slot_booking import Slot_Booking
from location import Location
from payment_page import Payment


from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.uix.root import Root
from kivy.core.text import LabelBase

import razorpay
# from crosswalk import WebView


# Window.size = (380, 720)
Window.size = (320, 580)

class ShotApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Shot"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        self.check_internet_status_timer = Timer(interval=5000, repeating=True, enabled=True,
                                                 tick=self.check_internet_status)
        print(platform)
        self.root = Root()
        self.root.push_replacement("main_sc")


    def check_internet_status(self, **event_args):
        try:
            anvil.server.call('check_internet_status')
            # If the check is successful, update UI or enable features as needed
        except anvil.server.AnvilWrappedError as e:
            self.handle_network_error(e)

    def handle_network_error(self, e):
        # Handle specific errors and display appropriate messages to the user
        self.show_validation_dialog("Network Error: Please check your internet connection.")

    def show_validation_dialog(self, message):
        # Create the dialog asynchronously
        Clock.schedule_once(lambda dt: self._create_dialog(message), 0)

    def _create_dialog(self, message):
        dialog = MDDialog(
            text=f"{message}",
            elevation=0,
        )
        dialog.open()



# Run the app
if __name__ == '__main__':
    LabelBase.register(name="Broboto", fn_regular="roboto/Roboto-Bold.ttf")
    ShotApp().run()
