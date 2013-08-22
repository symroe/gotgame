from django import forms

from title.models import ConsoleNetwork

from ..models import Player, PlayerConsoleNetwork

from .constants import PERSONAL_DETAILS_FIELDS, PLAYER_CONSOLE_FIELDS


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


class PlayerConsoleNetworkForm(forms.ModelForm):
    """
    Form to validate Player Console Network.
    """
    network = forms.ChoiceField(required=True, choices=ConsoleNetwork.objects.values_list('name', 'name'))

    class Meta:
        model = PlayerConsoleNetwork
        fields = PLAYER_CONSOLE_FIELDS

    def clean_network(self):
        network = self.cleaned_data.get('network')

        if network:
            network = ConsoleNetwork.objects.get(name=network)
        return network
