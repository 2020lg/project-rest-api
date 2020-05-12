from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset') # this generates the list of the URLs associated with our ViewSet
router.register('profile', views.UserProfileViewSet) # no need to specify base_name because our ViewSet has queryset object

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()), # it will match webserveraddress/api/hello-view
    path('', include(router.urls)) # '' means no prefix is required. 'router.urls' is a list of generated urls
]
