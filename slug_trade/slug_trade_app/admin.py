from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from . models import UserProfile, Item, Offer, Wishlist, ItemComment, ItemImage, OfferComment, ItemOffer, CashOffer


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):

    inlines = (UserProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['category', 'trade_options']
    list_display = ['name', 'get_name', 'price', 'category', 'trade_options', 'bid_counter', 'condition']

    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name


class ItemCommentAdmin(admin.ModelAdmin):
    list_display = ['get_item_name','time_stamp','comment']

    def get_name(self, obj):
        return obj.item.first_name + " " + obj.user.last_name

    def get_item_name(self, obj):
        return obj.item.name


class ItemImageAdmin(admin.ModelAdmin):
    list_display = ['get_item_name']

    def get_item_name(self, obj):
        return obj.item.name


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['wishlist_item_description','get_name']

    def get_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name


class OfferCommentAdmin(admin.ModelAdmin):
    list_display = ['get_item_name']

    def get_item_name(self, obj):
        return obj.item.name + obj.comment

#
# class ItemOfferAdmin(admin.ModelAdmin):
#     list_display = ['get_item_name']
#
#     def get_item_name(self, obj):
#         return obj.item.offer_item.name


class CashOfferAdmin(admin.ModelAdmin):
    list_display = ['get_item_name','offer_amount']

    def get_item_name(self, obj):
        return obj.item.name


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ItemComment, ItemCommentAdmin)
admin.site.register(OfferComment, OfferCommentAdmin)
admin.site.register(ItemOffer)
admin.site.register(CashOffer, CashOfferAdmin)
admin.site.register(Item, ItemAdmin)

admin.site.register(ItemImage, ItemImageAdmin)
admin.site.register(Wishlist, WishlistAdmin)
# admin.site.register(Picture)
admin.site.register(Offer)
