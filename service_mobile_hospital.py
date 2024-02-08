from form_validation import BaseRegistrationScreen


class MobileCareService(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super(MobileCareService, self).__init__(**kwargs)

    def validate_content(self):
        return super().validate_content()
