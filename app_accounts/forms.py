
from .models import Candidate
from django import forms
from django.core.exceptions import ValidationError
from django import forms
from captcha.fields import CaptchaField

    
# create a ModelForm
class CandiateForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Candidate
        fields = ['email', 'name', 'password', 'web_address','cover_letter','attachment','do_you_like_working',]


    def clean(self):
          cleaned_data=super().clean()
          if Candidate.objects.filter(email=cleaned_data["email"]).exists():
            raise ValidationError("The email is taken, please try another one")