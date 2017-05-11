"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegisterForm(forms.Form):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    # treba ce updateat bazu al nvm
    mail = forms.EmailField(max_length=254, widget = forms.EmailInput({
                                'class':'form-control',
                                'placeholder':'E-mail' })
                            )

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    pseudonime = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Pseudonime'}))
    favorite_books = forms.CharField(label=_("Password"),
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder':'Favorite book(s)'}))


#wil not use their's form, that is not good practice actually !
"""
CHOICES=[('1','Poetry'), ('2','Quote'), ('3', 'Short story')]

class PublishForm(forms.Form):    
    title = forms.CharField(max_length=254, required=True,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Title'}))

    genre = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect({
                                    
                              }))
"""