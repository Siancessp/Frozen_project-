from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address
from .models import AddressAdmin

admin.site.register(Address)
admin.site.register(AddressAdmin)