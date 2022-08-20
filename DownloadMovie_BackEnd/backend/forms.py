from django import forms
from .models import *


class SignupForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    country = forms.CharField()
    phone_number = forms.CharField()
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UploadFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = "__all__"


class AddCommentForm(forms.Form):
    film = forms.ModelChoiceField(queryset=Film.objects.all())
    text = forms.CharField(widget=forms.Textarea)
