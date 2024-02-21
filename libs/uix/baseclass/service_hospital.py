from form_validation import BaseRegistrationScreen


class HospitalService(BaseRegistrationScreen):
    
    def validate_content(self):
        super().validate_content('oxiclinic')