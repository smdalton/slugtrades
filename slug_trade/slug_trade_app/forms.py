from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from slug_trade_app.models import UserProfile, Item, ItemImage, CashOffer, OfferComment, ItemOffer

class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfile
        fields = (
            'bio',
            'on_off_campus'
        )

class UserModelForm(forms.ModelForm):
    class Meta():
        model = User
        fields = (
            'first_name',
            'last_name'
        )


class CashTransactionForm(forms.ModelForm):
    class Meta():
        model = CashOffer
        fields = (
            'offer_amount',
        )


class OfferCommentForm(forms.ModelForm):

    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'offer-comment'}))
    class Meta:
        model = OfferComment
        fields = (
            'comment',
            'item',
            'item_owner',
        )

    def __init__(self, *args, **kwargs):
        super(OfferCommentForm, self).__init__(*args, **kwargs)
        self.fields['item_owner'].widget = forms.HiddenInput()
        self.fields['item'].widget = forms.HiddenInput()


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
            'condition',
            'trade_options'
        )

    def __init__(self, *args, **kwargs):
        super(ClosetItem, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'value': 0,
                                                  'class': 'add-closet-wrapper-input'
                                                  })
        self.fields['description'].widget.attrs.update({'required': True,
                                                        'class': 'add-closet-wrapper-input'
                                                        })
        self.fields['category'].widget.attrs.update({'class': 'add-closet-wrapper-input'})
        self.fields['condition'].widget.attrs.update({'class': 'add-closet-wrapper-input'})

        self.fields['name'].widget.attrs.update({'required': True, 'class': 'add-closet-wrapper-input'})

        self.fields['trade_options'].widget.attrs.update({'required': True, 'class': 'add-closet-wrapper-input'})

class ClosetItemPhotos(forms.ModelForm):
    class Meta():
        model = ItemImage
        fields = (
            'image1',
            'image2',
            'image3',
            'image4',
            'image5'
        )
    def __init__(self, *args, **kwargs):
        super(ClosetItemPhotos, self).__init__(*args, **kwargs)
        self.fields['image1'].widget.attrs.update({'accept': 'image/*', 'class': 'add-closet-wrapper-input'})
        self.fields['image2'].widget.attrs.update({'accept': 'image/*', 'class': 'add-closet-wrapper-input'})
        self.fields['image3'].widget.attrs.update({'accept': 'image/*', 'class': 'add-closet-wrapper-input'})
        self.fields['image4'].widget.attrs.update({'accept': 'image/*', 'class': 'add-closet-wrapper-input'})
        self.fields['image5'].widget.attrs.update({'accept': 'image/*', 'class': 'add-closet-wrapper-input'})


class UserForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                             'id': 'username',
                                                             'name': 'fname',
                                                             'value' : 'MyCo',
                                                             'placeholder': 'Username',
                                                             'autocomplete':'given-name',
                                                             'required': True,
                                                             'maxlength': 256}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                              'id': 'first-name',
                                                              'name': 'fname',
                                                              'placeholder': 'First Name',
                                                              'autocomplete':'given-name',
                                                              'required': True,
                                                              'maxlength': 30,
                                                              'size': 5})) # firefox requires a size attribute to avoid overflowing the container

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                              'id': 'last-name',
                                                              'name': 'lname',
                                                              'placeholder': 'Last Name',
                                                              'autocomplete':'family-name',
                                                              'required': True,
                                                              'maxlength': 30,
                                                              'size': 5})) # firefox requires a size attribute to avoid overflowing the container

    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                              'name':'email',
                                                              'placeholder':'Email Address',
                                                              'autocomplete':'email',
                                                              'required': True,
                                                              'maxlength': 256,
                                                              'type': 'email'}))

    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                              'name':'password',
                                                              'placeholder':'Password',
                                                              'autocomplete':'password',
                                                              'type': 'password',
                                                              'required': True,
                                                              'maxlength': 256,
                                                              'size': 5})) # firefox requires a size attribute to avoid overflowing the container

    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                              'name':'password',
                                                              'placeholder':'Verification Password',
                                                              'type': 'password',
                                                              'required': True,
                                                              'maxlength': 256,
                                                              'size': 5})) # firefox requires a size attribute to avoid overflowing the container

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
        self.fields['bio'].widget.attrs.update({'placeholder': 'Write a little about yourself to build trust in your community...'})
        self.fields['bio'].widget.attrs.update({'class': 'form-input'})
        self.fields['on_off_campus'].widget.attrs.update({'required': True})
