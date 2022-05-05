from django import forms
from django.contrib.auth.models import User

from dal import autocomplete

from hknweb.candidate.models import BitByteActivity, OffChallenge


TEXT_AREA_STYLE = (
    "resize:none; border: none; border-radius: 0.2em; width: 23.6em; padding: 0.2em;"
)


class ChallengeRequestForm(forms.ModelForm):
    class Meta:
        model = OffChallenge
        fields = ["name", "officer", "proof"]
        widgets = {
            "officer": autocomplete.ModelSelect2(
                url="candidate:autocomplete_officer",
            ),
            "name": forms.Textarea(attrs={"style": TEXT_AREA_STYLE, "rows": 2}),
            "proof": forms.Textarea(attrs={"style": TEXT_AREA_STYLE, "rows": 3}),
        }


class BitByteRequestForm(forms.ModelForm):
    class Meta:
        model = BitByteActivity
        fields = ["participants", "proof"]
        widgets = {
            "participants": autocomplete.ModelSelect2Multiple(
                url="candidate:autocomplete_user"
            ),
            "proof": forms.Textarea(attrs={"style": TEXT_AREA_STYLE, "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super(BitByteRequestForm, self).__init__(*args, **kwargs)
        self.fields["participants"].queryset = User.objects.order_by("username")
