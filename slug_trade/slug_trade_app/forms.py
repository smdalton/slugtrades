from django import forms
from django.contrib.auth.models import User
from slug_trade_app.models import UserProfile, Item, ItemImage

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

class ClosetItem(forms.ModelForm):
    class Meta():
        model = Item
        fields = (
            'name',
            'price',
            'category',
            'description',
            'condition'
        )
    def __init__(self, *args, **kwargs):
        super(ClosetItem, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'value': 0})
        self.fields['description'].widget.attrs.update({'required': True})
        self.fields['name'].widget.attrs.update({'required': True})

class ClosetItemPhotos(forms.Form):
    image1 = forms.FileField(required=True)
    image2 = forms.FileField(required=False)
    image3 = forms.FileField(required=False)
    image4 = forms.FileField(required=False)
    image5 = forms.FileField(required=False)
    def __init__(self, *args, **kwargs):
        super(ClosetItemPhotos, self).__init__(*args, **kwargs)
        self.fields['image1'].widget.attrs.update({'required': True, 'accept': 'image/*'})
        self.fields['image2'].widget.attrs.update({'accept': 'image/*'})
        self.fields['image3'].widget.attrs.update({'accept': 'image/*'})
        self.fields['image4'].widget.attrs.update({'accept': 'image/*'})
        self.fields['image5'].widget.attrs.update({'accept': 'image/*'})

