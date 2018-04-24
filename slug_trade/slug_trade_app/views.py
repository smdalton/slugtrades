from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from slug_trade_app.forms import UserForm, SignupUserProfileForm
from . import models
from slug_trade_app.models import UserProfile


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

def signup(request):

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = SignupUserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            #create user
            created_user = user_form.save()

            created_user.username = created_user.email
            created_user.set_password(user_form.cleaned_data.get('password1'))
            created_user.save()

            #create extended profile
            created_profile = profile_form.save(commit=False)
            profile = UserProfile(
                user = created_user,
                profile_picture = request.FILES['profile_picture'],
                bio = created_profile.bio,
                on_off_campus = created_profile.on_off_campus
            )   
            profile.save()

            #authentication
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')

            authenticated = authenticate(
                username=email,
                password=password
            )
            #if user is authenticated log them in and redirect
            if authenticated:
                login(request, authenticated)
                return redirect('/home')
            else:
                print("not authenticated")
                return redirect('/home')
        else:
            print("NOT VALID")
            return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})

    else:
        user_form = UserForm()
        profile_form = SignupUserProfileForm()

        return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})
