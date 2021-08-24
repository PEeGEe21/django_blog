from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            # 'username',
            'email',
            # 'displayname',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'displayname',
            'bio',
            'birthday',
            'image',
            'coverimage',

        ]
        widgets = {
            # data-provide="datepicker" data-date-format="d-M-yyyy"
            'image': forms.FileInput(attrs={
                'class': 'dropify',
            }),
            'birthday': forms.DateInput(attrs={
                'data-provide': 'datepicker',
                'data-date-format': 'yyyy-mm-d'
            }),
            'coverimage': forms.FileInput(attrs={
                'class': 'dropify',
            }),
        }
        #dropify