import datetime

import requests
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from recipes.models import Profile


class CustomUserCreationForm(forms.ModelForm):
    """
        Custom UserCreationForm using Profile class
    """

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'date_of_birth',
            'country_choice',
            'avatar',
        )
        exclude = ['country', 'county_flag']

        widgets = {
            'avatar': forms.ClearableFileInput()
        }

    first_name = forms.CharField(label=_('Enter your firstname '),
                                 widget=forms.TextInput(attrs={'placeholder': 'Firstname'}),
                                 min_length=4,
                                 max_length=150,
                                 required=True)

    last_name = forms.CharField(label=_('Enter your lastname '),
                                widget=forms.TextInput(attrs={'placeholder': 'Lastname'}),
                                min_length=4,
                                max_length=150,
                                required=True)

    username = forms.CharField(label=_('Enter Username'),
                               min_length=4,
                               max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'username'}),
                               required=True)

    email = forms.EmailField(label=_('Enter email'),
                             widget=forms.TextInput(attrs={'placeholder': 'example@recipes.com'}),
                             required=True)

    password1 = forms.CharField(label=_('Enter password'),
                                widget=forms.PasswordInput(attrs={'placeholder': ''}),
                                min_length=8,
                                required=True)

    password2 = forms.CharField(label=_('Confirm password'),
                                widget=forms.PasswordInput(attrs={'placeholder': ''}),
                                min_length=8,
                                required=True)

    date_of_birth = forms.DateField(label=_('Date of birth'),
                                    required=True,
                                    widget=forms.SelectDateWidget(years=range(1900, datetime.date.today().year + 1)))

    avatar = forms.ImageField(label=_('Your avatar'), required=False)

    # getting country from resp api
    country_api_url = 'https://restcountries.eu/rest/v2/all'
    country_data = requests.get(url=country_api_url).json()

    country_choice = forms.ChoiceField(label=_('Your country'),
                                       choices=[(idx, val['name']) for idx, val in enumerate(country_data)],
                                       required=True)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError(_("Username already exists"))
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError(_("Email already exists"))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Password don't match"))

        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        return last_name

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['username'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password1'])

        # retrieve country index from form
        country_index = int(self.cleaned_data['country_choice'])

        # create specific Profile for this user
        user_profile = Profile()
        user_profile.user = user

        if self.cleaned_data['avatar'] != "":
            user_profile.avatar = self.cleaned_data['avatar']

        user_profile.date_of_birth = self.cleaned_data['date_of_birth']
        user_profile.country = self.country_data[country_index]['name']
        user_profile.country_flag = self.country_data[country_index]['flag']
        user_profile.save()

        return user
