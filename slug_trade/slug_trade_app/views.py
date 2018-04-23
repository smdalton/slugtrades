from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from slug_trade_app.forms import UserProfileForm, UserModelForm, ProfilePictureForm, ClosetItem, ClosetItemPhotos
from . import models
from slug_trade_app.models import ItemImage
# Create your views here.

def index(request):
    test = "This was passed from the backend!"
    print("in index view")
    return render(request, 'slug_trade_app/index.html',{'test':test})

def products(request):
    return render(request, 'slug_trade_app/products.html')

def profile(request):
    if request.user.is_authenticated():
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

def add_closet_item(request):
    if request.method == 'POST':
        form = ClosetItem(request.POST)
        photos = ClosetItemPhotos(request.POST, request.FILES)

        if form.is_valid():
            print('form is valid')
            item = form.save(commit=False)
            item.user = request.user
            form.save()

            if photos.is_valid():
                print('photos. is valid!')

                pics = []
                files = request.FILES

                if files.get('image1', False): pics.append(files['image1'])
                if files.get('image2', False): pics.append(files['image2'])
                if files.get('image3', False): pics.append(files['image3'])
                if files.get('image4', False): pics.append(files['image4'])
                if files.get('image5', False): pics.append(files['image5'])

                if len(pics) == 1:
                    insert = ItemImage(
                        item = item,
                        image1=pics[0]
                    )
                elif len(pics) == 2:
                    insert = ItemImage(
                        item = item,
                        image1=pics[0],
                        image2=pics[1]
                    )
                elif len(pics) == 3:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0],
                        image2=pics[1],
                        image3=pics[2]
                    )
                elif len(pics) == 4:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0],
                        image2=pics[1],
                        image3=pics[2],
                        image4=pics[3]
                    )
                elif len(pics) == 5:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0],
                        image2=pics[1],
                        image3=pics[2],
                        image4=pics[3],
                        image5=pics[4]
                    )

                insert.save()

        return redirect('/profile')

    else:
        form = ClosetItem()
        photos = ClosetItemPhotos()
        return render(request, 'slug_trade_app/add_closet_item.html', {'form': form, 'photos': photos})

