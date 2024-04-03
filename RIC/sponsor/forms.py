from django import forms
from django.core.validators import MinValueValidator
from .models import Sponsor, SponsorReg

class SponsorRegForm(forms.ModelForm):


    CATEGORY_CHOICES = (
            ('Title Sponsorship','Title Sponsorship'),
            ('Co Sponsorship','Co Sponsorship'),
            ('Platinum Sponsorship','Platinum Sponsorship'),
            ('Gold Sponsorship','Gold Sponsorship'),
            ('Silver Sponsorship','Silver Sponsorship'),
            ('Bronze Sponsorship','Bronze Sponsorship'),
            ('Other','Other'),
        )

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    logo = forms.ImageField(help_text='Please upload your company logo for display.')

    class Meta:
        model = SponsorReg
        fields = ['company_name', 'company_email', 'logo','poc_name','poc_email','poc_designation','poc_number', 'category', 'type_sponsor']