import re

from django import forms
from django.core.exceptions import ValidationError

PROFILE_URL_REGEX = re.compile(
    r"^\s*https?://(www\.)?csfd\.cz\/uzivatel\/(?P<uid>\d+)-"
)


class UserForm(forms.Form):
    uid = forms.URLField(
        label="Enter your profile URL",
        widget=forms.TextInput(
            attrs={
                "class": "box flex-grow mr-1",
                "placeholder": "https://www.csfd.cz/uzivatel/18708-polaroid/hodnoceni/",
            }
        ),
        required=True,
    )

    def clean_uid(self):
        profile_url = self.cleaned_data["uid"]
        m = PROFILE_URL_REGEX.match(profile_url)
        if m:
            return int(m.group("uid"))
        raise ValidationError("Invalid profile URL")
