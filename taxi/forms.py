from django import forms
from .models import Driver


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["license_number"]

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise forms.ValidationError(
                "The license number must be 8 characters long.")

        if (
                not license_number[:3].isalpha() or not
                license_number[:3].isupper()
        ):
            raise forms.ValidationError(
                "The first 3 characters must be capital letters."
            )

        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "The last 5 characters must be numbers."
            )

        return license_number
