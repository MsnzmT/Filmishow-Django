from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'country', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        Profile.objects.create(user=user, country=self.data['country'])
        return user
