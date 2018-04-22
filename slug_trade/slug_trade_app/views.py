from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from slug_trade_app.forms import UserForm, UserProfileForm
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
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid():
            print("1")
            #user
            created_user = user_form.save(commit=False)
            created_user.username = created_user.email
            created_user.set_password(created_user.password)
            created_user.save()
            print("2")

            #extended profile
            created_profile = profile_form.save(commit=False)
            print("3")
            created_profile.user = created_user
            print("4")
            created_profile.save()
            print("5")


            # # create user
            # username = request.POST['email']
            # first_name = request.POST['first_name']
            # last_name = request.POST['last_name']
            # email = request.POST['email']
            # password = request.POST['password1']
            #
            # user = User.objects.create_user(username=username,
            #                     first_name=first_name,
            #                     last_name=last_name,
            #                     email=email,
            #                     password=password)
            #
            # #extended
            # bio = request.POST['bio']
            # on_off_campus = request.POST['on_off_campus']
            #
            # user_profile = UserProfile.objects.create( user=user,
            #                     bio=bio,
            #                     on_off_campus=on_off_campus)



            user = authenticate(username=user_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, user)
            return redirect('/home')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

        return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})
