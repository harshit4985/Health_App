from form_validation import BaseRegistrationScreen


class OxyGymService(BaseRegistrationScreen):
    def validate_content(self):
        super().validate_content('oxigym')
