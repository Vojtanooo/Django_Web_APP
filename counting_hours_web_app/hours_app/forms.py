from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Day
from .choices import choice


class TimeInput(forms.TimeInput):
    input_type = "time"


class DayForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["working_day"] = forms.ChoiceField(
            choices=choice(user))

    class Meta:
        model = Day
        widgets = {"number_start": TimeInput(), "number_end": TimeInput()}
        fields = [
            "working_day",
            "number_start",
            "number_end",
            "result"
        ]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
