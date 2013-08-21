from django import forms

from ..models import Player

from .constants import PERSONAL_DETAILS_FIELDS


class PersonalDetailsForm(forms.ModelForm):
    """
    Form to validate Personal Details values.
    As the Player defines personal details fields as optional,
    this form is making them mandatory.
    """
    class Meta:
        model = Player
        fields = PERSONAL_DETAILS_FIELDS

    def __init__(self, *args, **kwargs):
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)

        # making fields mandatory
        for field_name in PERSONAL_DETAILS_FIELDS:
            self.fields[field_name].required = True
