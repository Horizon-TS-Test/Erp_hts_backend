from rest_framework import serializers
from . import models
import datetime
import json

#****************************************************************************#
#                  LÓGICA Y SERAILIZACION DE DATOS                           #
#****************************************************************************#
class ProvinceSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZERIALIZADORA PARA MODELO PROVINCE
    """
    cantons = serializers.SerializerMethodField()

    class Meta:
        model  = models.Province
        fields = ('id_province', 'description_province', 'cantons')
        read_only_fields = ('data_register', )


    def get_cantons(self, obj):
        """
        Obtenemos todos las parroquias del canton
        :param obj:
        :return:
        """
        cantons_data = models.Canton.objects.filter(province = obj.id_province)
        data_province   = []

        for item_canton in cantons_data:
            item_json = '{}'
            item_json = json.loads(item_json)
            item_json["description_canton"]= item_canton.description_canton
            item_json["id_canton"]= item_canton.id_canton
            data_province.append(item_json)

        return data_province


class CantonSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZERIALIZADORA PARA MODELO CANTON
    """
    parish = serializers.SerializerMethodField()
    class Meta:
        model  = models.Canton
        fields = ('id_canton', 'description_canton', 'province', 'parish')
        read_only_fields = ('data_register', )

    def get_parish(self, obj):
        """
        Obtenemos todos los datos de las parroquias
        :param obj:
        :return:
        """
        parish_data = models.Parish.objects.filter(canton = obj.id_canton)
        data_parish = []

        for item_parish in parish_data:
            item_json = '{}'
            item_json = json.loads(item_json)
            item_json["description"] = item_parish.description_parish
            item_json["id_parroquia"] = item_parish.id_parish
            data_parish.append(item_json)

        return data_parish


class ParishSerializer(serializers.ModelSerializer):
    """
    CLASE SERIALIZERIALIZADORA PARA MODELO CANTON
    """
    class Meta:
        model  = models.Parish
        fields = ('id_parish', 'description_parish', 'canton')
        read_only_fields = ('data_register', )

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
        fields  = ('id_enterprise', 'email', 'ruc', 'name', 'legal_agent', 'telephone', 'telephone_fax', 'movil_phone', 'address', 'neighborhood', 'postal_code', 'web_site', 'central_ent', 'parish' ,'busi_line', 'type_contrib', 'date_register')
        read_only_fields = ('date_register', )

class MarkSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model   = models.Mark
        fields  = ('id_mark', 'description',)
        read_only_fields  = ('date_update', 'date_register')

