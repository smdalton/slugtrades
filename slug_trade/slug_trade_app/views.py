from django.shortcuts import render
from django.contrib.auth.models import User
from slug_trade_app.forms import UserForm, UserProfileForm
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

def signup(request):

    signed_in = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST)

        print(user_form.is_valid())
        print(profile_form.is_valid())

        if user_form.is_valid() and profile_form.is_valid():
            print (user_form.cleaned_data['email'])
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile= profile_form.save(commit=False)

            profile.user = user

            profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            signed_in = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'slug_trade_app/signup.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'signed_in':signed_in})
