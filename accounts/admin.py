from django.contrib import admin
from .models import User, Seller
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


@admin.register(User)
class UserModelAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    # show jalali date in list display
    list_display = ['mobile', 'born_dateTime', 'id', "is_shope"]

    @admin.display(description='تاریخ ایجاد', ordering='created')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created).strftime('%a, %d %b %Y %H:%M:%S')



@admin.register(Seller)
class SellerModelAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    # show jalali date in list display
    list_display = ['user', 'id',]