from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from slug_trade_app.forms import UserProfileForm, UserModelForm, ProfilePictureForm
from . import models
# Create your views here.

def index(request):
    test = "This was passed from the backend!"
    print("in index view")
    return render(request, 'slug_trade_app/index.html',{'test':test})

def products(request):
    return render(request, 'slug_trade_app/products.html')

def profile(request):
    if request.user.is_authenticated():
        print(request.user)
        return render(request, 'slug_trade_app/profile.html', {'user': request.user})
    else:
        return render(request, 'slug_trade_app/not_authenticated.html')

def edit_profile(request):
    if request.method == 'POST':
        user_instance = User.objects.get(id=request.user.id)
        user_profile_instance = user_instance.userprofile
        user_form = UserModelForm(request.POST, instance=user_instance)
        user_profile_form = UserProfileForm(request.POST, instance=user_profile_instance)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
        if user_profile_form.is_valid():
            user_profile_form.save()
        if profile_picture_form.is_valid() and request.FILES['file']:
            user_profile_instance.profile_picture = request.FILES['file']
            user_profile_instance.save()
        return redirect('/profile')
    else:
        user = User.objects.get(id=request.user.id)
        user_form = UserModelForm(instance=user)
        user_profile = user.userprofile
        user_profile_form = UserProfileForm(instance=user_profile)
        profile_picture_form = ProfilePictureForm()
        return render(request, 'slug_trade_app/edit_profile.html', {
            'user_form': user_form, 
            'user_profile_form': user_profile_form, 
            'profile_picture_form': profile_picture_form,
            'user': request.user
            })
