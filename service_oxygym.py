from form_validation import BaseRegistrationScreen


class OxyGymService(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super(OxyGymService, self).__init__(**kwargs)

    def validate_content(self):
        return super().validate_content()
