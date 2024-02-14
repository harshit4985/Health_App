import json
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.uix.root import Root
from kivy.core.text import LabelBase
from login import Login

Window.size = (320, 580)


class ShotApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.login = Login()

        self.title = "Shot"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        self.root = Root()
        self.root.push_replacement("main_sc")

    def on_start(self):
        with open("logged_in_data.json", "r") as json_file:
            logged_in_data = json.load(json_file)
        if logged_in_data["logged_in"] == True:
            # with open('user_data.json', 'r') as file:
            #     user_info = json.load(file)
            # print(user_info['username'])
            # self.login.screen_change(user_info['username'],user_info["email"],user_info["password"],user_info["phone"],user_info["pincode"])
            self.root.load_screen("client_services")
            self.root.current = "client_services"
        else:
            self.root.load_screen("main_sc")
            self.root.current = "main_sc"

# Run the app
if __name__ == '__main__':
    LabelBase.register(name="Broboto", fn_regular="roboto/Roboto-Bold.ttf")
    ShotApp().run()
