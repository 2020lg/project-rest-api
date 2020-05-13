from rest_framework import serializers
from profiles_api import models # lets us access UserProfile model we created


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10) # similar to Django forms, take care of validation rules


class UserProfileSerializer(serializers.ModelSerializer): # ModelSerializer has extra functionality
    """Serializes a user profile object"""

    class Meta: # for ModelSerializer, you need to create a meta class to point to a specific model in the project
        model = models.UserProfile # sets serializer to point to our model
        fields = ('id', 'email', 'name', 'password') # tuple of fields we want to make accessible in our model
        extra_kwargs = {
            'password': { # keys of the dict are the fields that you want to add custom configuration to
                'write_only': True, # when we create a password field for our model, set it to write_only=True
                'style': {'input_type': 'password'} # can only see starts or dots while typing in the password
            }
        }

    def create(self, validated_data):
        """
        Create and return a new user.
        Overwrites the default DRF create() function of the Object Manager
        So the password gets created as a hash not a clear text password by default.
        """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """
        Handle updating user account.
        Overwrites the default DRF update() function to hash the user's password when updating.
        Otherwise, If a user updates their profile, the password field is stored in cleartext,
        and they are unable to login.
        """

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on') # by default Django adds key 'id' to all models we create
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }
