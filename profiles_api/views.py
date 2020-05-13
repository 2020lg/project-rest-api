from rest_framework.views import APIView
from rest_framework.response import Response # standard Response object that's returned when from APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication # token authentication is a type of authentication we use
                                                              # for users to authenticate themselves with our API.
                                                              # It works by generating a random token string when the user logs in
                                                              # and then every request we make to that API that we need to authenticate
                                                              # we add this token string to the request ie it's effectively a password
                                                              # to check that every request that's made is authenticated correctly
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken # DRF comes with an Auth Token view out the box
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated # blocks access to the entire endpoint unless the user is authenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView): # creates a new class based on APIView class that Django REST framework provides
                             # allows us to define the application logic for our endpoint that we are going to
                             # assign to this view. You define a URL which is our endpoint and then you assign
                             # this view and DJango REST framework handles it by callin gthe appropriate function
                             # in the view HTTP request you make.
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP method as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview}) # Response needs to contain a dict or list because it converts Response into JSON

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name') # retrieves the name field
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None): # usually has an id (primary key) of an object you are updating
        """Handle updating an entire object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """
        Handle a partial update of an object,
        based on the fields provided in the request
        """
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet): # ModelViewSet is specifically designed for managing models through our API
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all() # DRF knows the standard functions that you would want to perform on ModelViewSet: create, list, update, partial_update, destroy.
                                                # DRF takes care of all that by assigning a a serializer_class to a model Serializer and queryset
    authentication_classes = (TokenAuthentication,) # tuple, you can add all authentication classes here, but we'll be using AuthToken
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,) # tuple
    search_fields = ('name', 'email',) # searchable fields


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # ObtainAuthToken class doesn't by default enable itself in the browsable Django admin site.
                                                             # So we need to overwrite this class and customize it so it's visible in the browsable API
                                                            # and it makes us easier for us to test. We need to add renderer_classes manually.


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer): # DRF's function that allows you to customize the behavior for creating objects through a model ViewSet. When a request gets made to our ViewSet, it gets passed to our serializer class and validated, and then the serializer.save() is called by default.
        """Sets the user profile to the logged-in user"""
        serializer.save(user_profile=self.request.user) # when a new object is created (HTTP POST call), DRF calls perform_create() and it passes in the serializer that we are using to create the object.
                                                        # The serializer is a model serializer so it has a save() function assigned to it. That save() function is used to save the contents of the serializer to an object in the DB.
                                                        # We are calling serializer.save() and we are passing in an additional keyword for the 'user_profile'. This gets passed in in addition to all the items in the serializer that've benn validated.
                                                        # Request object is an object that gets passed into all viewsets every time a request is made.
                                                        # Request contains all the details about the request being made to the viewset.
                                                        # If the user has authenticated, then the request has a user associated to the authenticated user. So the user field is added whenever the user is authenticated.
                                                        # If the user is not authenticated, it's just set to an anonymous user account.
