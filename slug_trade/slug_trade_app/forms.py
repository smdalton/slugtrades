from django import forms
from django.contrib.auth.models import User
from slug_trade_app.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    User.user_name = "e@gmail.com"

    class Meta():
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('profile_picture', 'bio', 'on_off_campus')
