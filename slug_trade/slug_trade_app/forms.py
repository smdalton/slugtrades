from django import forms
from django.contrib.auth.models import User
from slug_trade_app.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('bio', 'on_off_campus')


class UserModelForm(forms.ModelForm):
    class Meta():
        model = User
        fields = (
            'first_name',
            'last_name'
        )

class ProfilePictureForm(forms.Form):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({
            'accept': 'image/*'
        })