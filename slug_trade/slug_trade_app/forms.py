from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from slug_trade_app.models import UserProfile

class UserForm(UserCreationForm):

    username = forms.CharField(
        error_messages={'required': 'Username is required', 'max_length': 'Username name too long'}, required=True,
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'username', 'name': 'fname', 'value' : 'MyCo', 'placeholder': 'Username','autocomplete':'given-name'}))

    first_name = forms.CharField(
        error_messages={'required': 'First name is required', 'max_length': 'First name too long'}, required=True,
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-input', 'name': 'fname','placeholder': 'First Name','autocomplete':'given-name'}))

    last_name = forms.CharField(
        error_messages={'required': 'Last name is required', 'max_length': 'Last name too long'}, required=True,
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-input','name': 'fname','placeholder': 'Last Name','autocomplete':'family-name'}))

    email = forms.CharField(
        error_messages={'required': 'Email address is required', 'max_length': 'Email is too long'}, required=True,
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-input','name':'email','placeholder':'Email Address','autocomplete':'email'}))

    password1 = forms.CharField(
        error_messages={'required': 'Password required', 'max_length': 'Password is too long'}, required=True,
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-input','name':'password','placeholder':'Password','autocomplete':'password'}))

    password2 = forms.CharField(
        error_messages={'required': 'Verification password required', 'max_length': 'Password is too long'}, required=True,
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-input','name':'password','placeholder':'Verification Password'}))

    def clean_email(self):
        username = self.cleaned_data["email"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("An account is already active with that email.")


    class Meta:
        model = User
        # exclude = ('username',)
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = (
            'profile_picture',
            'bio',
            'on_off_campus'
        )
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'accept': 'image/*'})
        self.fields['profile_picture'].widget.attrs.update({'required': True})
