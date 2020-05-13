from django.contrib import admin
from profiles_api import models

admin.site.register(models.UserProfile) # tells Django admin to register our UserProfile model with the admin site so makes it accessible through admin interface
admin.site.register(models.ProfileFeedItem)
