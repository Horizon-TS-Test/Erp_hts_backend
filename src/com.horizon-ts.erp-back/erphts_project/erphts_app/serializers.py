from rest_framework import serializers
from . import models
import datetime
import json

#****************************************************************************#
#                  LÓGICA Y SERAILIZACION DE DATOS                           #
#****************************************************************************#

class PersonSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZADORA DE DATOS PARA LA TABLA PERSONA
    """
    class Meta:
        model = models.Person
        fields = ('id_person', 'identification_card', 'name', 'last_name', 'age', 'telephone', 'cell_phone', 'address', 'active', 'birthdate', 'date_register', 'date_update')
        read_only_fields = ('active', 'date_register', 'date_update')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    """

    person = PersonSerializer()
    
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'password', 'media_profile', 'profile_path', 'date_register', 'date_update', 'person')
        read_only_fields = ('date_update',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        CREATE AND RETURN A NEW USER.
        """
        print("validated_data...", validated_data)
        _data_person = validated_data.pop('person')
        person = models.Person.objects.create(**_data_person)
        media_image = validated_data.get('media_profile', None)
        _profile_path = validated_data.get('profile_path', None)
        if media_image is None:
            user = models.UserProfile(
                email= validated_data['email'],
                profile_path = _profile_path,
                person= person
            )
        else :
            user = models.UserProfile(
                email=validated_data['email'],
                profile_path =  _profile_path,
                person=person,
                media_profile= media_image
            )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        UPDATE AND RETURN A USER.
        """
        person = validated_data.get("person")
        instance.email                          = validated_data.get('email', instance.email)
        instance.media_profile                  = validated_data.get('media_profile', instance.media_profile)
        instance.profile_path                   = validated_data.get('profile_path', instance.profile_path)
        instance.is_active                      = validated_data.get('is_active', instance.is_active)
        instance.date_update                    = datetime.datetime.now()
        if validated_data.get('password') is not None:
            instance.set_password(validated_data.get('password', instance.password))
        instance.person.age                     = person.get("age", instance.person.age)
        instance.person.identification_card     = person.get("identification_card", instance.person.identification_card)
        instance.person.name                    = person.get("name", instance.person.name)
        instance.person.last_name               = person.get("last_name", instance.person.last_name)
        instance.person.telephone               = person.get("telephone", instance.person.telephone)
        instance.person.cell_phone              = person.get("cell_phone", instance.person.cell_phone)
        instance.person.birthdate               = person.get("birthdate", instance.person.birthdate)
        instance.person.address                 = person.get("address", instance.person.address)
        #instance.person.parish                  = person.get("parish", instance.person.parish)
        instance.person.active                  = validated_data.get('is_active', instance.is_active)
        instance.person.date_update             = datetime.datetime.now()
        instance.person.save()
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = models.Activity
        fields = ('id_activity', 'description')

class BusinessLineSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = models.BusinessLine
        fields = ('id_busi_line', 'description', 'activity')

class TypeContributorSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = models.TypeContributor
        fields = ('id_type_contributor', 'description')

class EnterpriseSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model   = models.Enterprise
        fields  = ('id_enterprise', 'email', 'ruc', 'name', 'legal_agent', 'telephone', 'telephone_fax', 'movil_phone', 'address', 'neighborhood', 'postal_code', 'web_site', 'central_ent', 'busi_line', 'type_contrib', 'date_register')
        read_only_fields = ('date_register', )




