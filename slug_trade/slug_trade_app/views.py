from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .models import UserProfile
from slug_trade_app.forms import UserProfileForm, UserModelForm, ProfilePictureForm, ClosetItem, ClosetItemPhotos, UserForm, SignupUserProfileForm
from . import models
from slug_trade_app.models import ItemImage, Item
from slug_trade_app.models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
debug = False


def index(request):
    test = "This was passed from the backend!"
    if debug:
        print("in index view")
    return render(request, 'slug_trade_app/index.html',{'test':test})

def products(request):
    if request.user.is_authenticated():
        items_list = ItemImage.objects.exclude(item__user=request.user)
        paginator = Paginator(items_list, 6) # Show 6 contacts per page
        page = request.GET.get('page', 1)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return render(request, 'slug_trade_app/products.html', {'items': items})
    else:
        return render(request, 'slug_trade_app/not_authenticated.html')

# debug route
def show_users(request):
    users = User.objects.all()

    # for each user we want to get the
    if debug:
        for item in users:
            print(item.userprofile)
    return render(request, 'slug_trade_app/users.html', {'users': users})
#
# def show_items(request):
#     # get items and item images by user
#     items = models.Item.objects.all()
#     users = User.objects.all()
#     images = models.ItemImage.all()
#
#     final_dict = {}
#
#     # for user in User.objects.all():
#     #     final_dict[user] = {}
#     #     for item in models.Item.objects.filter(user=user):
#     #         final_dict[user][item] = []
#     #         for image in models.ItemImage.objects.filter(item=item):
#     #             final_dict[user][item].append(image.image1.url)
#
#     return render(request, 'slug_trade_app/items.html',
#                   {
#                     'items': items,
#                     'users': users,
#                     'images': images
#                   })
#



def profile(request):
    if request.user.is_authenticated():
        if debug:
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

def add_closet_item(request):
    if request.method == 'POST':
        form = ClosetItem(request.POST)
        photos = ClosetItemPhotos(request.POST, request.FILES)

        if form.is_valid():
            print('form is valid')
            item = form.save(commit=False)
            item.user = request.user
            if item.price < 0:
                item.price = 0
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
        if request.user.is_authenticated():
            form = ClosetItem()
            photos = ClosetItemPhotos()
            return render(request, 'slug_trade_app/add_closet_item.html', {'form': form, 'photos': photos})
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
