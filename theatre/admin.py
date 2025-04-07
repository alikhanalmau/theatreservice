from django.contrib import admin
from .models import User, Event, ExcursionOrder, Review
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Event)
admin.site.register(ExcursionOrder)
admin.site.register(Review)
