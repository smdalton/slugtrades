from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from slug_trade_app.models import UserProfile

class UserForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'username', 'name': 'fname', 'value' : 'MyCo', 'placeholder': 'Username','autocomplete':'given-name', 'required': True, 'maxlength': 256}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'name': 'fname','placeholder': 'First Name','autocomplete':'given-name', 'required': True, 'maxlength': 30}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input','name': 'fname','placeholder': 'Last Name','autocomplete':'family-name', 'required': True, 'maxlength': 30}))

    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input','name':'email','placeholder':'Email Address','autocomplete':'email', 'required': True, 'maxlength': 256}))

    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input','name':'password','placeholder':'Password','autocomplete':'password', 'type': 'password', 'required': True, 'maxlength': 256}))

    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input','name':'password','placeholder':'Verification Password', 'type': 'password', 'required': True, 'maxlength': 256}))

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


class SignupUserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = (
            'profile_picture',
            'bio',
            'on_off_campus'
        )
    def __init__(self, *args, **kwargs):
        super(SignupUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'accept': 'image/*'})
        self.fields['profile_picture'].widget.attrs.update({'required': True})
        self.fields['bio'].widget.attrs.update({'required': True})
        self.fields['on_off_campus'].widget.attrs.update({'required': True})
