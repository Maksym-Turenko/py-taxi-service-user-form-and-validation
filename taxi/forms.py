import re

from django import forms
from django.core.validators import RegexValidator

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}\d{5}$",
                message=(
                    "The license number must consist of 8 characters: "
                    "the first 3 characters are capital letters, "
                    "the last 5 characters are numbers."
                )
            )
        ]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Driver
        fields = [
            "username",
            "first_name",
            "last_name",
            "license_number",
            "password"
        ]

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        pattern = r"^[A-Z]{3}\d{5}$"

        if not re.match(pattern, license_number):
            raise forms.ValidationError(
                "The driver's license number must consist of 8 characters: "
                "the first 3 characters are capital letters, "
                "the last 5 characters are numbers."
            )
        return license_number

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.set_password(self.cleaned_data["password"])
        if commit:
            driver.save()
        return driver


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["model", "manufacturer", "drivers"]
        widgets = {
            "drivers": forms.CheckboxSelectMultiple,
        }
