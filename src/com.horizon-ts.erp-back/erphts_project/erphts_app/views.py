from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken 
from .constants.erp_init_constants import ErpHtsConstants
from . import serializers
from . import models

# Create your views here.

class ProvinceViewSet(viewsets.ModelViewSet):
    """
       HANDLES CREATING, READING AND UPDATING PROVINCE.
       """
    serializer_class = serializers.ProvinceSerializer
    queryset = models.Province.objects.all().order_by("description_province")
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_province')
    pagination_class = None


class CantonViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING CANTON.
    """
    serializer_class = serializers.CantonSerializer
    queryset = models.Canton.objects.all().order_by("description_canton")
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_canton')
    pagination_class = None

    def get_queryset(self):
        """
        Filtros para consultas de cantones de una parroquia.
        :return: List
        """
        req = self.request
        qrOp = req.query_params.get(ErpHtsConstants.FILTER_PROVINCE)

        print ("province", qrOp)
        if qrOp is None:
            return models.Canton.objects.all()
        else:
            return models.Canton.objects.filter(province = qrOp)


class ParishViewSet(viewsets.ModelViewSet):
    """
    HANDLES CREATING, READING AND UPDATING TYPEACTION.
    """
    serializer_class = serializers.ParishSerializer
    queryset = models.Parish.objects.all().order_by("description_parish")
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description_parish')
    pagination_class = None

    def get_queryset(self):
        """
        Filtros para consultas de parroquias de una provincia.
        :return: List
        """
        req = self.request
        qrOp = req.query_params.get(ErpHtsConstants.FILTER_CANTON)

        print ("canton", qrOp)
        if qrOp is None:
            return models.Parish.objects.all()
        else:
            return models.Parish.objects.filter(canton = qrOp)


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