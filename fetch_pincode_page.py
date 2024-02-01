from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import json
from urllib.request import urlopen

Builder.load_file("client_services1.kv")
class Location(MDScreen):
    def client_services(self):
        app = MDApp.get_running_app()
        app.root.transition.direction = "right"
        app.root.current = "client_services"
    def fetch_pincode(self):
        pincode = self.ids.pincode.text
        if not pincode or len(pincode) != 6:
            self.ids.pincode.error = True
            self.ids.pincode.helper_text = "Invalid Pincode (6 digits required)"
        else:
            self.ids.pincode.error = False
            self.ids.pincode.helper_text = ""
            self.ids.pincode.text = ""
            app = MDApp.get_running_app()
            app.root.transition.direction = "right"
            app.root.current = "client_services"
    def get_location(self):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        pincode = data["postal"]
        self.ids.pincode.text = pincode