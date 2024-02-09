from kivy import platform

import anvil
from anvil import Timer
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.uix.root import Root
from kivy.core.text import LabelBase


# Window.size = (380, 720)
Window.size = (320, 580)


class ShotApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Shot"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        # self.check_internet_status_timer = Timer(interval=5000, repeating=True, enabled=True,
        #                                          tick=self.check_internet_status)
        print(platform)
        self.root = Root()
        self.root.push_replacement("main_sc")

    # def check_internet_status(self, **event_args):
    #     try:
    #         anvil.server.call('check_internet_status')
    #         # If the check is successful, update UI or enable features as needed
    #     except anvil.server.AnvilWrappedError as e:
    #         self.handle_network_error(e)
    #
    # def handle_network_error(self, e):
    #     # Handle specific errors and display appropriate messages to the user
    #     self.show_validation_dialog("Network Error: Please check your internet connection.")
    #
    # def show_validation_dialog(self, message):
    #     # Create the dialog asynchronously
    #     Clock.schedule_once(lambda dt: self._create_dialog(message), 0)
    #
    # def _create_dialog(self, message):
    #     dialog = MDDialog(
    #         text=f"{message}",
    #         elevation=0,
    #     )
    #     dialog.open()


# Run the app
if __name__ == '__main__':
    LabelBase.register(name="Broboto", fn_regular="roboto/Roboto-Bold.ttf")
    ShotApp().run()
