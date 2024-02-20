from kivymd.uix.screen import MDScreen

from form_validation import BaseRegistrationScreen


class HospitalServiceDoc(BaseRegistrationScreen):
    def file_manager_open(self, field_id):
        super().file_manager_open(field_id)

    # def submit(self):
    #     self.manager.push_replacement("service_register_form2", "right")


