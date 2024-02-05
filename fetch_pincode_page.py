from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
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
        try:
            import requests
            r = requests.get('https://get.geojs.io/')
            ip_request = requests.get('https://get.geojs.io/v1/ip.json')
            ipAdd = ip_request.json()['ip']
            print(ipAdd)
            url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
            geo_request = requests.get(url)
            geo_data = geo_request.json()
            print(geo_data)
            # pincode = data["postal"]
            # self.ids.pincode.text = pincode
        except Exception:
            self.show_validation_dialog("No Internet Connection")

    def show_validation_dialog(self, message):
        # Create the dialog asynchronously
        Clock.schedule_once(lambda dt: self._create_dialog(message), 0)

    def _create_dialog(self, message):
        dialog = MDDialog(
            text=f"{message}",
            elevation=0,
        )
        dialog.open()
