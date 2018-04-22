from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from slug_trade_app.models import UserProfile

class UserForm(UserCreationForm):
    # email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    # def save(self, commit=True):
    #     user = super(UserForm, self).save(commit=False)
    #     user.username = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.email = self.cleaned_data['email']
    #
    #     if commit:
    #         user.save()
    #
    #     return user


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('profile_picture', 'bio', 'on_off_campus')











# from django import forms
# from django.contrib.auth.models import User
# from slug_trade_app.models import UserProfile
#
# class UserForm(forms.ModelForm):
#
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta():
#         model = User
#         fields = ('username','first_name', 'last_name', 'email', 'password')
#
# class UserProfileForm(forms.ModelForm):
#     class Meta():
#         model = UserProfile
#         fields = ('profile_picture', 'bio', 'on_off_campus')
