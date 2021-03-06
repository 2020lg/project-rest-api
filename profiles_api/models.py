from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings # used to retrieve settings from settings.py file


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email: # if an empty string or null
            raise ValueError("User must have an email address")

        email = self.normalize_email(email) # makes the second half (domain portion) of email all lowercase
        user = self.model(email=email, name=name)

        user.set_password(password) # sets the user’s password to the given raw string, taking care of the password hashing
                                    # when the password is None, the password will be set to an unusable password
        user.save(using=self._db) # supports multiple DBs

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password) # when you call a class method, 'self' gets automatically passed in

        user.is_superuser = True # automatically created by PermissionsMixin
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True) # email column
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' # overwrites the default USERNAME_FIELD to be email, not user name
    REQUIRED_FIELDS = ['name'] # USERNAME_FIELD is required by default, name is an additional required field

    def get_full_name(self): # class method
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self): #recommended for Django models
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, # best practice to retrieve UserProfile from settings.py. YOu may decide that you want to switch out the UserProfile model as out default auth model and you want to use Django default model. If you hard code it to the name of the model , then you'd have to manually update all the foreign keys
        on_delete=models.CASCADE # tell the DB what to do if the remote field is deleted. If user profile is deleted, then all the related feed items are also deleted (cascade)
    )
    status_text = models.CharField(max_length=255) # contains the text of the feed update
    created_on = models.DateTimeField(auto_now_add=True) # every time the feed item is created, the time stamp is auto added

    def __str__(self): # string representation of our model to tell Python what to do when we convert a model instance into a string. 
        """Return the model as a string"""
        return self.status_text
