from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken 
from . import serializers
from . import models

# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class    = serializers.PersonSerializer
    queryset            = models.Person.objects.all()
    filter_backends     = (filters.SearchFilter,) 
    search_fields       = ('identification_card', 'name', 'last_name',)

    def perform_create(self, serializer):
        serializer.save(active = True)

class LoginViewSet(viewsets.ViewSet):
    """
    """
    serializers_class = AuthTokenSerializer

    def create(self, request):
        _response = ObtainAuthToken().post(request)
        _useremail = request.data.get('username')

        if _useremail is not None:
            _user = models.UserProfile.objects.filter(email = _useremail)
        
        if _user is not None:
            print ("User profile", _user)
        
        return _response
    
    def get_authenticate_header(self, request):
        pass

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    """

    serializer_class   = serializers.UserProfileSerializer
    queryset            = models.UserProfile.objects.all()
    filter_backend      = (filters.SearchFilter,)
    search_fields       = ('email',)

class ActivityViewSet(viewsets.ModelViewSet):
    """
    """

    serializer_class   = serializers.ActivitySerializer
    queryset            = models.Activity.objects.all()
    filter_backend      = (filters.SearchFilter,)
    search_fields       = ('description',)

class BusinessLineViewSet(viewsets.ModelViewSet):
    """
    """

    serializer_class   = serializers.BusinessLineSerializer
    queryset            = models.BusinessLine.objects.all()
    filter_backend      = (filters.SearchFilter,)
    search_fields       = ('description', )

class TypeContributorViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class    = serializers.TypeContributorSerializer
    queryset            = models.TypeContributor.objects.all()
    filter_backend      = (filters.SearchFilter)
    search_fields       = ('description', )

class EnterpriseViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class   = serializers.EnterpriseSerializer
    queryset            = models.Enterprise.objects.all()
    filter_backend      = (filters.SearchFilter)
    search_fields       = ('ruc', 'name', 'email', )

class MarkViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class      = serializers.MarkSerializer
    queryset              = models.Mark.objects.all()
    filter_backend        = (filters.SearchFilter)
    search_fields         = ("description", )