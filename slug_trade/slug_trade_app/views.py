from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .forms import UserProfileForm, UserModelForm, ProfilePictureForm, ClosetItem, ClosetItemPhotos, \
    UserForm, SignupUserProfileForm, CashTransactionForm, OfferCommentForm
from . import models
from .models import ItemImage, Item, Wishlist
from .models import UserProfile, ITEM_CATEGORIES, TRADE_OPTIONS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pprint
# Create your views here.
debug = False



def index(request):
    items = Item.objects.all()[:4]
    images = [ItemImage.objects.get(item=item).get_image_list() for item in items]
    items_and_images = zip(items, images)

    books = Item.objects.filter(category="BO")[:4]
    b_images = [ItemImage.objects.get(item=book).get_image_list() for book in books]
    books_and_images = zip(books,b_images)

    popular = Item.objects.all().order_by('-bid_counter')[:4]
    p_images = [ItemImage.objects.get(item=p).get_image_list() for p in popular]
    popular_and_images = zip(popular,p_images)

    recent = Item.objects.all().order_by('-time_stamp')[:4]
    r_images = [ItemImage.objects.get(item=r).get_image_list() for r in recent]
    recent_and_images = zip(recent,r_images)

    categories = [
        { 'name': 'All', 'value': 'All' }
    ]
    types = [
        { 'name': 'All', 'value': 'All' }
    ]

    for value, name in ITEM_CATEGORIES:
        categories.append({ 'name': name, 'value': value})

    for value, name in TRADE_OPTIONS:
        types.append({ 'name': name, 'value': value })

    return render(request, 'slug_trade_app/index.html', {
        'items_and_images': items_and_images,
        'books_and_images': books_and_images,
        'popular_and_images': popular_and_images,
        'recent_and_images': recent_and_images,
        'categories': categories,
        'types': types
    })


def products(request):

    categories = []
    category_values = []
    selected_values = []

    types = []
    type_values = []
    selected_types = []

    order_by = [
        { 'name': 'Popular', 'value': 'Popular' },
        { 'name': 'Recent', 'value': 'Recent' }
    ]

    order_by_selected = 'Nothing'

    default_order_name = 'Recent'
    default_order_filter = '-item__time_stamp'


    for value, name in ITEM_CATEGORIES:
        categories.append({ 'name': name, 'value': value})
        category_values.append(value)

    for value, name in TRADE_OPTIONS:
        types.append({ 'name': name, 'value': value })
        type_values.append(value)


    items_list = ItemImage.objects.all()

    if request.GET.get('categories', False):
        selected_values = []
        for key, values in request.GET.lists():
            if key =='categories':
                for value in values:
                    selected_values.append(value)

        for category in category_values:
            if category not in selected_values:
                items_list = items_list.exclude(item__category=category)

    if request.GET.get('types', False):
        selected_types = []
        for key, values in request.GET.lists():
            if key =='types':
                for value in values:
                    selected_types.append(value)

        for type in type_values:
            if type not in selected_types:
                items_list = items_list.exclude(item__trade_options=type)

    if request.GET.get('order_by', False):
        if request.GET['order_by'] == 'Popular':
            items_list = items_list.order_by('-item__bid_counter')
            order_by_selected = 'Popular'
        elif request.GET['order_by'] == 'Recent':
            items_list = items_list.order_by('-item__time_stamp')
            order_by_selected = 'Recent'
    else:
        items_list = items_list.order_by(default_order_filter)
        order_by_selected = default_order_name

    item_count = items_list.count()
    paginator = Paginator(items_list, 12) # Alter the second parameter to change number of items per page
    page = request.GET.get('page', 1)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'slug_trade_app/products.html', {
    'items': items,
    'categories': categories,
    'selected_values': selected_values,
    'types': types,
    'selected_types': selected_types,
    'item_count': item_count,
    'order_by': order_by,
    'order_by_selected': order_by_selected
    })


# Easy CBV replacement
class UserView(ListView):
    model = User
    template_name = 'slug_trade_app/users.html'
    context_object_name = 'users'


# detail CBV
class ItemDetailView(DetailView):
    model = Item


def item_details(request, item_id=None):
    """
    primary purpose is to show user more about a specific item, and allow them to bid on it
    :param request: http request
    :param item_id: regexed number from url string that is item to inspect's item-id
    :return: a template with detailed information on the item with item_id, and the ability
    to continue further in the transaction process of trading
    """
    if not item_id:
        return redirect('/products')


    # load the item assosciated with item_id
    bid_item = models.Item.objects.get(id=item_id)
    # filter out all images that have a foreign key to the item we just found
    item_images = models.ItemImage.objects.get(item=item_id).get_image_list()
    # load the currently logged in users items

    # assembled the users items into a useful dictionary object

    # send that dictionary object to the template for rendering

    # remove spaces from trade type and makes lowercase for url. ex - Cash Only -> cash_only
    trade_type_name = bid_item.get_trade_options_display()
    trade_type_name = trade_type_name.replace(" ", "_").lower()

    return render(request, 'slug_trade_app/item_details.html', {'inspect_item': bid_item,
                                                                'item_photos': item_images,
                                                                'item_id': item_id,
                                                                'trade_type': trade_type_name,
                                                                })


def my_placed_offers(request):

    my_cash_offers = []
    my_trade_offers = []
    my_free_offers = []

    # get all offers that have been placed by request.user
    my_cash_offers_list = models.CashOffer.objects.filter(original_bidder=request.user)
    for cash_offer in my_cash_offers_list:
        my_cash_offers.append({
            'item_name': cash_offer.item_bid_on.name,
            'item_picture': cash_offer.item_bid_on.get_images(),
            'amount': cash_offer.offer_amount,
            'trade_details': '/trade_details/?thing=whatever&thing2=otherThing'
        })

    my_item_offers = models.ItemOffer.objects.filter(original_bidder=request.user)
    work_dict = {}
    for item_offer in my_item_offers:
        if item_offer.item_bid_on not in work_dict:
            work_dict[item_offer.item_bid_on] = []
            work_dict[item_offer.item_bid_on].append(item_offer.item_bid_on.get_images())
        else:
            work_dict[item_offer.item_bid_on].append(item_offer.item_bid_on.get_images())

    for item in work_dict:
        my_trade_offers.append(
            {
                'item_name': item.name,
                'item_image': item.get_images(),
                'bid_items_list': work_dict[item],
                'trade_details': '/trade_details/?Owner=test'
            }
        )

    my_free_offers_list = models.OfferComment.objects\
        .filter(comment_placed_by=request.user)\
        .filter(item__trade_options='2')
    for free_offer in my_free_offers_list:
        my_free_offers.append({
            'item_name': free_offer.item.name,
            'item_image': free_offer.item.get_images(),
            'comment': free_offer.comment,
        })

    print(my_trade_offers)
    return render(request, 'slug_trade_app/my_offers.html',
                  {
                    'viewing_offers_on_my_items': False,
                    'viewing_my_placed_offers': True,
                    'my_cash_offers': my_cash_offers,
                    'my_trade_offers': my_trade_offers,
                    'my_free_offers': my_free_offers,
                  })


def my_received_offers(request):

    # check for authentication
    if not request.user.is_authenticated:
        return redirect('/signup')

    # load my items as a list of items
    items = models.Item.objects.filter(user=request.user).all()
    # initialize dicts to be populated with offers
    cash_offers = []
    trade_offers = []
    free_offers = []

    for item in items:

        # cash items
        if item.trade_options == '0':
            cash_offer_list = models.CashOffer.objects.filter(item_bid_on=item).all()
            for offer in cash_offer_list:
                print(item.price)
                cash_offers.append(
                    {
                        'item_name': item.name,
                        'item_price': item.price,
                        'item_image': item.get_images(),
                        'bidders_name': offer.original_bidder.first_name,
                        'bid_amount': offer.offer_amount,
                        'details_link': '/trade_details/?Owner=test&Item=id',
                    }
                )

        # trade items
        if item.trade_options == '1':
            # add the key for the current item to the trade offers_dict
            trade_offer_list = models.ItemOffer.objects.filter(item_bid_on=item).all()
            # sort the offers into lists of offers by individual users
            work_dict = {}
            for offer in trade_offer_list:
                if offer.original_bidder not in work_dict:
                    work_dict[offer.original_bidder] = []
                    work_dict[offer.original_bidder].append(offer.item_bid_with.get_images())
                else:
                    work_dict[offer.original_bidder].append(offer.item_bid_with.get_images())

            # build the front-end object for rendering
            for user in work_dict:
                trade_offers.append(
                    {
                        'item_name': item.name,
                        'item_image': item.get_images(),
                        'bidders_name': user.first_name,
                        'bid_items_list': work_dict[user],
                        'trade_details': '/trade_details/?Owner=test&Item=id'
                    }
                )


        # free items

        if item.trade_options == '2':
            free_comments = models.OfferComment.objects.filter(item=item).all()

            work_dict = {}
            for comment in free_comments:
                if comment.comment_placed_by not in work_dict:
                    work_dict[comment.comment_placed_by] = []
                    work_dict[comment.comment_placed_by].append({
                        'item_name': item.name,
                        'item_image': item.get_images(),
                        'comment': comment.comment,
                        'comment_placed_by':  comment.comment_placed_by.first_name,
                    })
                else:
                    work_dict[comment.comment_placed_by].append({
                        'item_name': item.name,
                        'item_image': item.get_images(),
                        'comment': comment.comment,
                        'comment_placed_by': comment.comment_placed_by.first_name,
                    })

            if len(free_comments) > 0:
                # add it to the list because there are comments
                for commenter in work_dict:
                    free_offers.append(work_dict[commenter])


    return render(request, 'slug_trade_app/my_offers.html',
                  {
                    'viewing_offers_on_my_items': True,
                    'viewing_my_placed_offers': False,
                    'cash_offers': cash_offers,
                    'trade_offers': trade_offers,
                    'free_offers': free_offers,

                  })


def cash_transaction(request, item_id=None):

    if not request.user.is_authenticated:

        return render(request, 'slug_trade_app/not_authenticated.html')
    # declare outside scope of try block
    sale_item = None
    try:
        sale_item = Item.objects.get(id=item_id)
        # check to see if
        if sale_item.user == request.user:
            return HttpResponse("Looks like you own this item, sadly you can't buy your own stuff!\
                                <a href='/products'>go back to products page</a>")
        if sale_item.trade_options is not '0':
            # redirect them to item details that is appropriate for this specific item
            return HttpResponse(("This is not a trade item <a href='/item_details/{}'>\
                                Go to this items details page</a>").format(item_id))
    except Exception as e:
        print(e)
        # send them a life preserver if they get lost
        return HttpResponse('This item does not exist <a href="/home">Go to home page<a>')

    if request.method == 'POST':
        # Process the form submission
        completed_cash_offer_form = CashTransactionForm(request.POST)
        completed_offer_comment_form = OfferCommentForm(request.POST)
        completed_cash_offer_form.is_valid()
        completed_offer_comment_form.is_valid()

        print(request.POST['offer_amount'])
        print(request.POST['comment'])

        item_owner = sale_item.user

        if request.POST['comment']:
            # make a comment object
            comment = models.OfferComment(
                item=sale_item,
                item_owner=item_owner,
                comment_placed_by=request.user,
                comment=request.POST['comment']
            )
            comment.save()
            print("comment detected {}".format(request.POST['comment']))
        else:
            print('no comment')

        # print(request.POST['offer_amount'])
        if request.POST['offer_amount']:
            # make a cash offer object
            cash_offer = models.CashOffer(
                item_bid_on=sale_item,
                offer_amount=request.POST['offer_amount'],
                item_owner=item_owner,
                original_bidder=request.user
            )
            cash_offer.save()
            print("offer_amount detected {}".format(request.POST['offer_amount']))


        return redirect('/my_placed_offers')

    else:
        # render the appropriate transaction form
        item = Item.objects.get(id=item_id)

        offer_comment_form = OfferCommentForm()
        # import cash offer form
        cash_transaction_form = CashTransactionForm()
        # TODO: Believe the below sale_item declaration is redundant (shadows clone in top scope)
        # too little time to test at the moment
        sale_item = Item.objects.get(id=item_id)
        print('>>>>>>>>>>> cash', sale_item.trade_options)
        sale_item_image = models.ItemImage.objects.get(item=item_id).get_image_list()[0]
        return render(request, 'slug_trade_app/transaction.html', {
            'transaction_type': 'cash',
            'sale_item': sale_item,
            'sale_item_image': sale_item_image,
            'cash_transaction_form': cash_transaction_form,
            'offer_comment_form': offer_comment_form
        })


def trade_transaction(request, item_id=None):
    # item_list = Item.objects.filter(user__id=request.user.id)
    """

    :param request: request from a user, maybe be a get or a post
    :param item_id: id for item which the transaction is being placed on
    :return: redirect to home page, successfully save the transaction in the database with the models
    """

    # If user enters wrong id for some reason the item will not exist and redirect them to home
    # ensure that no incorrect querys ever end up in this view
    if not request.user.is_authenticated:

        return render(request, 'slug_trade_app/not_authenticated.html')
    try:
        sale_item = Item.objects.get(id=item_id)
        if sale_item.trade_options is not '1':
            # redirect them to item details that is appropriate for this specific item
            return HttpResponse("This is not a trade item\
                                 <a href='/item_details/{}'>Go to this items details page</a>".format(item_id))
    except Exception as e:
        print(e)
        # send them a life preserver if they get lost
        return HttpResponse('This item does not exist <a href="/home">Go to home page<a>')

    if sale_item.user == request.user:
        return HttpResponse("Looks like you own this item, sadly you can't snag your own stuff!\
                             <a href='/products'>go back to products page</a>")

    # preload the offer comment form with an offer comment object

    offer_comment_form = OfferCommentForm(request.POST)

    # get the currently logged in users items for sending to the template or the form
    logged_in_users_items = models.Item.objects.filter(user=request.user).values()

    for item in logged_in_users_items:
        if len(item['description']) > 90:
            words = item['description'].split(' ')
            new_description = ''
            for word in words:
                if len(new_description + word) >= 90:
                    new_description = new_description[:-1]
                    new_description += '...'
                    break;
                else:
                    new_description += word + ' '
            item['description'] = new_description

    for item_representation_dict in logged_in_users_items:
        # fore each get the image link for representation in the template
        item_representation_dict['image'] = models.ItemImage.objects.get(item=item_representation_dict['id'])\
            .get_image_list()[0]

    if request.method == 'POST':

        # process all of the item_id strings in form body into ints
        items_selected_for_trade = [int(item) for item in request.POST.getlist("selected-item")]

        for item in items_selected_for_trade:
            # print(item)
            # these are the items that were checked in the form, so for each we must add an item trade offer
            new_item_offer = models.ItemOffer(
                item_bid_on=sale_item,
                item_bid_with=models.Item.objects.get(id=item),
                item_owner=sale_item.user,
                original_bidder=request.user
            )
            new_item_offer.save()

        # call this to generate the cleaned data dict for the form
        offer_comment_form.is_valid()

        # specify a default value for the comment as None, so that if there is a problem the code will terminate
        comment = offer_comment_form.cleaned_data.get('comment', None)
        if comment:
            # create an offer comment and save it to the database
            new_comment = models.OfferComment(
                item=sale_item,
                item_owner=sale_item.user,
                comment_placed_by=request.user,
                comment=comment,
            )
            new_comment.save()

        return redirect('/my_placed_offers')

        # # TODO:// offer comment is not currently working correctly


    else:
        # prepare the multi-field item form for rendering

        sale_item_image = models.ItemImage.objects.get(item=item_id).get_image_list()[0]

        offer_comment_form = OfferCommentForm()
        all_forms = []

        return render(request,
                      'slug_trade_app/transaction.html',
                      {'transaction_type': 'trade',
                       'sale_item': sale_item,
                       'offer_comment_form': offer_comment_form,
                       'logged_in_users_items': logged_in_users_items,
                       'sale_item_image': sale_item_image,
                       })


def free_transaction(request, item_id=None):

    offer_comment_form = OfferCommentForm(request.POST)

    if not request.user.is_authenticated:
        return render(request, 'slug_trade_app/not_authenticated.html')


    free_item = None
    try:
        # check existence
        free_item = Item.objects.get(id=item_id)
        if free_item.user == request.user:
            return HttpResponse("Looks like you own this item, sadly you can't buy your own stuff!\
                                 <a href='/products'>go back to products page</a>")

        # check free
        if free_item.trade_options is not '2':
            # redirect them to item details that is appropriate for this specific item
            return HttpResponse("This is not a trade item <a href='/item_details/{}'>\
                                Go to this items details page</a>".format(item_id))
    except Exception as e:
        print(e)
        # send them a life preserver if they get lost
        return HttpResponse('This item does not exist <a href="/home">Go to home page<a>')

    if request.method == 'POST':
        if request.POST['comment']:
            # make a comment object
            comment = models.OfferComment(
                item=free_item,
                item_owner=free_item.user,
                comment_placed_by=request.user,
                comment=request.POST['comment']
            )
            comment.save()

            return redirect('/my_placed_offers')
    else:
        sale_item_image = models.ItemImage.objects.get(item=item_id).get_image_list()[0]

        return render(request, 'slug_trade_app/transaction.html', {'transaction_type': 'free',
                                                                   'sale_item': free_item,
                                                                   'sale_item_image': sale_item_image,
                                                                   'offer_comment_form':offer_comment_form
                                                                   })


def public_profile_inspect(request, user_id):
    """
        :param request: http request obj
        :param user_id: database key for specific user to load details about
        REQUIREMENTS: user_id exists in the database and it corresponds correctly
        to a specific user (numbers outside
        :return: render template
    """

    if request.user.is_authenticated:

        # verify that the given user_id is in the database, and if no prompt a redirect
        if not User.objects.filter(id=user_id).exists():
            return HttpResponse('<h1>No user exists for your query <a href="/">Go home</a></h1>')

        if request.user.is_authenticated and int(user_id) == int(request.user.id):
            return redirect('/profile')

        # get the user model object
        user_to_view = User.objects.get(id=user_id)

        # get all of the items for the given user
        items_list = Item.objects.filter(user__id=user_id)

        item_count = items_list.count()

        paginator = Paginator(items_list, 6)
        page = request.GET.get('page', 1)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        images= [ItemImage.objects.get(item=item).get_image_list() for item in items]
        items_and_images = zip(items,images)

        wishlist = Wishlist.objects.filter(user=User.objects.get(id=user_id))

        return render(request, 'slug_trade_app/profile.html', {
                          'user_to_view': user_to_view,
                          'public': True,
                          'item_data': items_and_images,
                          'wishlist': wishlist,
                          'show_add_button': False,
                          'items': items,
                          'item_count': item_count
                      })

    else:
        return render(request, 'slug_trade_app/not_authenticated.html')


def profile(request):
    """
        profile is the view that handles authenticated users who have logged in
        by default it displays relevant information about the user, if no user
        is logged in, it will redirect to a sign-up/broken page
    """
    if request.user.is_authenticated:
        if request.method == 'POST' and not request.POST['description'].isspace() and not request.POST['description'] == '':
            # if the wishlist item already exists in the wishlist, do not add it again
            try:
                existing_item = Wishlist.objects.get(user=request.user,
                                                     wishlist_item_description=request.POST['description'])
            except Wishlist.DoesNotExist:
                item = Wishlist(
                    user=request.user,
                    wishlist_item_description=request.POST['description']
                )
                item.save()
                return redirect('/profile?item_added=True')

        wishlist = Wishlist.objects.filter(user=request.user)
        items_list= Item.objects.filter(user__id=request.user.id)

        item_count = items_list.count()

        paginator = Paginator(items_list, 10)
        page = request.GET.get('page', 1)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        images= [ItemImage.objects.get(item=item).get_image_list() for item in items]
        items_and_images = zip(items,images)

        return render(request, 'slug_trade_app/profile.html', {
                    'user_to_view': request.user,
                    'public': False,
                    'item_data': items_and_images,
                    'wishlist': wishlist,
                    'show_add_button': True,
                    'item_added': request.GET.get('item_added', False),
                    'items': items,
                    'my_profile': True,
                    'item_count': item_count
                })
    else:
        return render(request, 'slug_trade_app/not_authenticated.html')


@csrf_exempt
def delete_from_wishlist(request):
    Wishlist.objects.get(id=request.POST['id']).delete()
    return HttpResponse('Deleted!')


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
        if request.user.is_authenticated:
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
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')


def add_closet_item(request):
    if request.method == 'POST':
        form = ClosetItem(request.POST)
        pics = []
        files = request.FILES
        # pic_names = ['image1','image2','image3','image4','image5']
        # pics = [files.get(name) for name in pic_names if files.get(name, False)]

        if files.get('image1', False): pics.append(files['image1'])
        if files.get('image2', False): pics.append(files['image2'])
        if files.get('image3', False): pics.append(files['image3'])
        if files.get('image4', False): pics.append(files['image4'])
        if files.get('image5', False): pics.append(files['image5'])


        image1 = pics.pop(0)

        if len(pics) >= 1:
            image2 = pics.pop(0);
        else:
            image2 = None
        if len(pics) >= 1:
            image3 = pics.pop(0);
        else:
            image3 = None
        if len(pics) >= 1:
            image4 = pics.pop(0);
        else:
            image4 = None
        if len(pics) >= 1:
            image5 = pics.pop(0);
        else:
            image5 = None

        photos_data = {
            'image1': image1,
            'image2': image2,
            'image3': image3,
            'image4': image4,
            'image5': image5
        }

        photos = ClosetItemPhotos(request.POST, photos_data)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            if item.price < 0:
                item.price = 0
            form.save()

            if photos.is_valid():
                insert = ItemImage(
                    item = item,
                    image1 = image1,
                    image2 = image2,
                    image3 = image3,
                    image4 = image4,
                    image5 = image5
                )
                insert.save()

        return redirect('/profile')

    else:
        if request.user.is_authenticated:
            form = ClosetItem()
            photos = ClosetItemPhotos()
            return render(request, 'slug_trade_app/add_closet_item.html', {'form': form, 'photos': photos})
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')

def edit_closet_item(request):
    if request.method == 'POST':
        item_images_instance = ItemImage.objects.get(id=request.POST.get('id', None))
        item_instance = item_images_instance.item

        form = ClosetItem(request.POST, instance=item_instance)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            if item.price < 0:
                item.price = 0
            form.save()

            files = request.FILES
            temps = request.POST

            image1 = files.get('image1', '')
            image2 = files.get('image2', '')
            image3 = files.get('image3', '')
            image4 = files.get('image4', '')
            image5 = files.get('image5', '')

            temp1 = temps.get('temp-image1', '')
            temp2 = temps.get('temp-image2', '')
            temp3 = temps.get('temp-image3', '')
            temp4 = temps.get('temp-image4', '')
            temp5 = temps.get('temp-image5', '')

            if image1:
                image1_action = 'update'
            elif not image1 and not temp1:
                image1_action = 'delete'
            else:
                image1_action = 'none'

            if image2:
                image2_action = 'update'
            elif not image2 and not temp2:
                image2_action = 'delete'
            else:
                image2_action = 'none'

            if image3:
                image3_action = 'update'
            elif(not image3 and not temp3):
                image3_action = 'delete'
            else:
                image3_action = 'none'

            if image4:
                image4_action = 'update'
            elif(not image4 and not temp4):
                image4_action = 'delete'
            else:
                image4_action = 'none'

            if image5:
                image5_action = 'update'
            elif not image5 and not temp5:
                image5_action = 'delete'
            else:
                image5_action = 'none'

            images = {
                'image1': image1,
                'image2': image2,
                'image3': image3,
                'image4': image4,
                'image5': image5
            }

            actions = {
                'image1': image1_action,
                'image2': image2_action,
                'image3': image3_action,
                'image4': image4_action,
                'image5': image5_action
            }

            update = ItemImage.objects.get(item=Item.objects.get(id=request.GET.get('id', None)))

            if actions['image1'] == 'update':
                update.image1 = images['image1']
            elif actions['image1'] == 'delete':
                update.image1 = None

            if actions['image2'] == 'update':
                update.image2 = images['image2']
            elif actions['image2'] == 'delete':
                update.image2 = None

            if actions['image3'] == 'update':
                update.image3 = images['image3']
            elif actions['image3'] == 'delete':
                update.image3 = None

            if actions['image4'] == 'update':
                update.image4 = images['image4']
            elif actions['image4'] == 'delete':
                update.image4 = None

            if actions['image5'] == 'update':
                update.image5 = images['image5']
            elif actions['image5'] == 'delete':
                update.image5 = None

            update.save()

            pics = []

            update = ItemImage.objects.get(item=Item.objects.get(id=request.GET.get('id', None)))

            if update.image1: pics.append(update.image1)
            if update.image2: pics.append(update.image2)
            if update.image3: pics.append(update.image3)
            if update.image4: pics.append(update.image4)
            if update.image5: pics.append(update.image5)

            if len(pics)>=1:
                update.image1 = pics.pop(0)
            else:
                update.image1 = None

            if len(pics)>=1:
                update.image2 = pics.pop(0)
            else:
                update.image2 = None

            if len(pics)>=1:
                update.image3 = pics.pop(0)
            else:
                update.image3 = None

            if len(pics)>=1:
                update.image4 = pics.pop(0)
            else:
                update.image4 = None

            if len(pics)>=1:
                update.image5 = pics.pop(0)
            else:
                update.image5 = None

            update.save()

        return redirect('/profile')

    else:
        if request.user.is_authenticated:
            item = Item.objects.get(id=request.GET.get('id', None))
            if request.user == item.user:
                item_images = ItemImage.objects.get(item=item)
                form = ClosetItem(instance=item)
                photos = ClosetItemPhotos(instance=item_images)
                return render(request, 'slug_trade_app/add_closet_item.html', {'form': form, 'photos': photos, 'id': item_images.id, 'edit': True, 'images': item_images, 'item_id': item.id})
            else:
                return HttpResponse("You can't edit someone else's items.")
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')

@csrf_exempt
def delete_closet_item(request):
    item = Item.objects.get(id=request.POST['item_id'])
    item_images = ItemImage.objects.get(item=item)
    item_images.delete()
    item.delete()
    return HttpResponse('Deleted!')



    form = ClosetItem(request.POST, instance=item_instance)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        if item.price < 0:
            item.price = 0
        form.save()

        files = request.FILES
        temps = request.POST

        image1 = files.get('image1', '')
        image2 = files.get('image2', '')
        image3 = files.get('image3', '')
        image4 = files.get('image4', '')
        image5 = files.get('image5', '')

        temp1 = temps.get('temp-image1', '')
        temp2 = temps.get('temp-image2', '')
        temp3 = temps.get('temp-image3', '')
        temp4 = temps.get('temp-image4', '')
        temp5 = temps.get('temp-image5', '')

        if image1:
            image1_action = 'update'
        elif not image1 and not temp1:
            image1_action = 'delete'
        else:
            image1_action = 'none'

        if image2:
            image2_action = 'update'
        elif not image2 and not temp2:
            image2_action = 'delete'
        else:
            image2_action = 'none'

        if image3:
            image3_action = 'update'
        elif(not image3 and not temp3):
            image3_action = 'delete'
        else:
            image3_action = 'none'

        if image4:
            image4_action = 'update'
        elif(not image4 and not temp4):
            image4_action = 'delete'
        else:
            image4_action = 'none'

        if image5:
            image5_action = 'update'
        elif not image5 and not temp5:
            image5_action = 'delete'
        else:
            image5_action = 'none'

        images = {
            'image1': image1,
            'image2': image2,
            'image3': image3,
            'image4': image4,
            'image5': image5
        }

        actions = {
            'image1': image1_action,
            'image2': image2_action,
            'image3': image3_action,
            'image4': image4_action,
            'image5': image5_action
        }

        update = ItemImage.objects.get(item=Item.objects.get(id=request.GET.get('id', None)))

        if actions['image1'] == 'update':
            update.image1 = images['image1']
        elif actions['image1'] == 'delete':
            update.image1 = None

        if actions['image2'] == 'update':
            update.image2 = images['image2']
        elif actions['image2'] == 'delete':
            update.image2 = None

        if actions['image3'] == 'update':
            update.image3 = images['image3']
        elif actions['image3'] == 'delete':
            update.image3 = None

        if actions['image4'] == 'update':
            update.image4 = images['image4']
        elif actions['image4'] == 'delete':
            update.image4 = None

        if actions['image5'] == 'update':
            update.image5 = images['image5']
        elif actions['image5'] == 'delete':
            update.image5 = None

        update.save()

        pics = []

        update = ItemImage.objects.get(item=Item.objects.get(id=request.GET.get('id', None)))

        if update.image1: pics.append(update.image1)
        if update.image2: pics.append(update.image2)
        if update.image3: pics.append(update.image3)
        if update.image4: pics.append(update.image4)
        if update.image5: pics.append(update.image5)

        if len(pics)>=1:
            update.image1 = pics.pop(0)
        else:
            update.image1 = None

        if len(pics)>=1:
            update.image2 = pics.pop(0)
        else:
            update.image2 = None

        if len(pics)>=1:
            update.image3 = pics.pop(0)
        else:
            update.image3 = None

        if len(pics)>=1:
            update.image4 = pics.pop(0)
        else:
            update.image4 = None

        if len(pics)>=1:
            update.image5 = pics.pop(0)
        else:
            update.image5 = None

        update.save()

        return redirect('/profile')

    else:
        if request.user.is_authenticated:
            item = Item.objects.get(id=request.GET.get('id', None))
            if request.user == item.user:
                item_images = ItemImage.objects.get(item=item)
                form = ClosetItem(instance=item)
                photos = ClosetItemPhotos(instance=item_images)
                return render(request, 'slug_trade_app/add_closet_item.html', {'form': form, 'photos': photos, 'id': item_images.id, 'edit': True, 'images': item_images, 'item_id': item.id})
            else:
                return HttpResponse("You can't edit someone else's items.")
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/products')

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = SignupUserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # create user
            created_user = user_form.save()

            created_user.username = created_user.email
            created_user.set_password(user_form.cleaned_data.get('password1'))
            created_user.save()

            # create extended profile
            created_profile = profile_form.save(commit=False)

            profile = UserProfile(
                user=created_user,
                profile_picture=request.FILES['profile_picture'],
                bio=created_profile.bio,
                on_off_campus=created_profile.on_off_campus
            )
            profile.save()

            # authentication
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')

            authenticated = authenticate(
                username=email,
                password=password
            )
            # if user is authenticated log them in and redirect
            if authenticated:
                login(request, authenticated)
                return redirect('/products')
            else:
                return redirect('/home')
        else:
            return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})

    else:
        user_form = UserForm()
        profile_form = SignupUserProfileForm()

        return render(request, 'slug_trade_app/signup.html', {'user_form': user_form,
                                                              'profile_form': profile_form,
                                                              })
