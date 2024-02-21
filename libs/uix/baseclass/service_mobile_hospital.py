from form_validation import BaseRegistrationScreen


class MobileCareService(BaseRegistrationScreen):
    def validate_content(self):
        super().validate_content('oxitaxi')