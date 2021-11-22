from django.forms import ModelForm

from .models import Polls


class CreatePollForm(ModelForm):
    class Meta:
        model = Polls
        fields = ["question", "option_one", "option_two", "option_three"]
