from django import forms
from django.core.exceptions import ValidationError

from csfd_export.scraper import EXAMPLE_PROFILE_URL, ScraperError, parse_uid


class UserForm(forms.Form):
    uid = forms.URLField(
        label="Enter your profile URL",
        widget=forms.TextInput(
            attrs={
                "class": "box flex-grow mr-1",
                "placeholder": EXAMPLE_PROFILE_URL,
            }
        ),
        required=True,
    )

    def clean_uid(self) -> int:
        try:
            return parse_uid(self.cleaned_data["uid"])
        except ScraperError as e:
            raise ValidationError(e.args[0])
