from django import forms
from .models import Driver
import re


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise forms.ValidationError(
                "The license number must contain 8 characters."
            )

        if not re.match(r"^[A-Z]{3}", license_number):
            raise forms.ValidationError(
                "The first 3 characters must be capital letters."
            )

        if not re.match(r"[0-9]{5}$", license_number):
            raise forms.ValidationError(
                "The last 5 characters must be numbers."
            )

        return license_number
