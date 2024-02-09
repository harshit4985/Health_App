from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen


class ProfileCard(MDFloatLayout, CommonElevationBehavior):
    pass

class Profile(MDScreen):
    def profile_back(self):
        self.manager.pop()
        screen = self.manager.get_screen('client_services')
        screen.ids.nav_drawer.set_state("close")
