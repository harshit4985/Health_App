from form_validation import BaseRegistrationScreen


class MobileCareServiceDoc(BaseRegistrationScreen):
    def file_manager_open(self, field_id):
        super().file_manager_open(field_id)