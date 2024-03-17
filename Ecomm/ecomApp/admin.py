from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Otp,CustomerCoupon,Product,Catagory

class CustomUserAdmin(UserAdmin):
    list_display = ('id',  'phone_number','name','address','profile_photo', 'is_active', 'is_staff')
    search_fields = ('id',  'phone_number')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),  # Removed 'username' from fields
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    filter_horizontal = ()  # Remove references to 'groups' and 'user_permissions'
    ordering = ('phone_number',)  # Change ordering to use existing field

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Otp)
admin.site.register(CustomerCoupon)
admin.site.register(Product)
admin.site.register(Catagory)

