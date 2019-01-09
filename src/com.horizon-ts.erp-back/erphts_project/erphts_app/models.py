"""
DOCUMENTACION DE ESTE MODULO.
El presente script contiene informacion sobre los modelos de la base de datos para la aplicacion erphts.
por medio de este escript se puede gestionar el modelo fisico de la DB para la creacion, modificacion e eliminacion
de tablas, hay que tomar en cuenta reglas de disenio de DB relacional para al momento del modelamiento de la db ya que
el modelo se creara tomando en cuenta cardinalidad sin garantizar que el proceso de migracion se lo realize correctamente
segun su disenio si no se ha definido bien los modelos de acuerdo a las reglas de DRF para persistencia de datos, para evitar incovenientes
se recomienda leer la documentacion de modelos para DRF.
"""

__author__      = "Dennys Ivan Moyón Gunsha"
__copyright__   = "Copyreight 2018, Horizon Technology Solutions"
__credits__     = ["Horizon Tecnology Solutions", "Dennys Moyón", "Patricia Allauca"]
__license__     = "GPL"
__version__     = "0.1.0"
__maintainer__  = "Consultores HTS"
__email__       = "dmoyon@horizon-ts.com"
__status__      = "Develop"

from django.db import models
# FOR AUTHENTICATION:
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# PERMISSIONS FOR SPECIFIC USERS TO LET THEM TO DO SOMETHING:
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
import uuid

# Create your models here.
# MANAGER CLASS TO HANDLE ALL MODELS:


def make_id_model():
    """
    Permite Generar UUID para los registros de la DB.
    :return: uuid clava unica para registro de la DB
    """
    return uuid.uuid4()

class UserProfileManager(BaseUserManager):
    """
    HELPS DJANGO WORK WITH UR CUSTOM USER MODEL.
    """

    def create_user(self, email, person, password=None):
        """
        CREATES A NEW USER PROFILE OBJECTS
        """

        if not email:
            raise ValueError('Users must have an email address.')

        # CONVERTS EVERY EMAIL CHARACTER TO LOWERCASE:
        # REF: https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email
        email = self.normalize_email(email)
        user = self.model(email=email, person = person)

        # NEXT FUNCTIONS WILL ENCRYPT PASSWORD FOR US, RETURNING A HASH TO BE
        # STORED IN OUR DATABASE:
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, person):
        """
        CREATES AND SAVES A NEW SUPERUSER WITH GIVEN DETAILS:
        """
        user = self.create_user(email, password, person)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

#--------------------------------------------------------------------------------------#
#---------------DEFINICION DE MODELOS DE BASE DE DATOS PARA APLICACION erphts----------#
#--------------------------------------------------------------------------------------#
class Province(models.Model):
    """
    MODELO PROVINCIA QUE REPRESENTA A LA TABLA erphts_app_province DE LA BASE DE DATOS erphts_DB
    """
    id_province = models.UUIDField(primary_key=True, unique=True, default=make_id_model, editable=False)
    description_province = models.CharField(max_length=100, unique=True)
    date_register = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return  self.description_province


class Canton(models.Model):
    """
    MODELO CANTON QUE REPRESENTA A LA TABLA erphts_app_canton DE LA BASE DE DATOS erphts_DB
    """
    id_canton = models.UUIDField(primary_key=True, unique=True, default=make_id_model, editable=False)
    description_canton = models.CharField(max_length=100, unique=True)
    date_register = models.DateTimeField(default = timezone.now)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, related_name = "cantones_p")

    def __str__(self):
        return  self.description_canton


class Parish(models.Model):
    """
    MODELO CANTON QUE REPRESENTA A LA TABLA erphts_app_canton DE LA BASE DE DATOS erphts_DB
    """
    id_parish = models.UUIDField(primary_key=True, unique=True, default=make_id_model, editable=False)
    description_parish = models.CharField(max_length=100, unique=True)
    date_register = models.DateTimeField(default = timezone.now)
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, null=True, related_name = "parish_c")

    def __str__(self):
        return self.description_parish


class Person(models.Model):
    """
    MODELO PERSON QUE REPRESENTA A LA TABLA erphts_app_person EN LA DB.
    """
    id_person           = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
    age                 = models.IntegerField()
    identification_card = models.CharField(max_length=10)
    name                = models.CharField(max_length=50)
    last_name           = models.CharField(max_length=50)
    telephone           = models.CharField(max_length=10)
    cell_phone          = models.CharField(max_length=10, null=True)
    address             = models.CharField(max_length=75)
    active              = models.BooleanField(default=True)
    birthdate           = models.DateTimeField(null=True, blank=True)
    date_register       = models.DateTimeField(default = timezone.now)
    date_update         = models.DateTimeField(null=True, blank=True)
    parish              = models.ForeignKey(Parish, on_delete = models.CASCADE, null = True, related_name = "parish_person")
    #user_register = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #user_update = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_pr")

    def get_full_name(self):
        """
        USED TO GET A USER'S FULL NAME
        """
        return self.name + self.last_name

    def get_short_name(self):
        """
        USED TO GET A USER'S SHORT NAME
        """
        return self.name

    def __str__(self):
        """
        DEVULVE EL IDENTIFICAR O CL DE LA PERSONA
        :return:
        """
        return '%s: %s' % (self.name, self.identification_card)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    MODELO USERPROFILE REPRESENTA A LA TABLA erphts_app_userprofile DE LA DB erphts_DB
    """

    # DJANGO MODELS REF: https://docs.djangoproject.com/en/1.11/topics/db/models/
    email               = models.EmailField(max_length=100, unique=True)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    last_login          = models.DateTimeField(null=True, blank=True)
    date_register       = models.DateTimeField(default = timezone.now)
    date_update         = models.DateTimeField(null=True, blank=True)
    person              = models.OneToOneField('person', related_name='userProfile', on_delete=models.CASCADE, null=True)
    media_profile       = models.ImageField(upload_to='medios_profile', default='default_profile.png', null=True)
    profile_path        = models.TextField(default = '/images/default-profile.png')
    objects             = UserProfileManager()

    USERNAME_FIELD = 'email'  # EMAIL IS REQUIRED BY DEFAULT

    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.email



class Profile(models.Model):
    """
    MODELOS PROFILE QUE REPRESENTA A LA TABLA erphts_app_profile  EN LA DB erphts_db
    """

    id_profile          = models.UUIDField(primary_key=True, default=make_id_model, editable=False, unique=True)
    description         = models.CharField(max_length=75)
    date_register       = models.DateTimeField(default = timezone.now)
    date_update         = models.DateTimeField(null=True, blank=True)
    active              = models.BooleanField(default=True)
    user_register       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_register_pf")
    user_update         = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_pf")
    users = models.ManyToManyField(
                    UserProfile,
                    through='ProfileUser',
                    through_fields=('profile', 'user'))
    
    def __str__(self):
        """
        DJANGO USES THIS WHEN IT NEEDS TO CONVERT THE OBJECT TO A STRING
        """
        return self.description




class ProfileUser(models.Model):
    """
    MODELO PROFILEUSER REPRESENTA A LA TABLA erphts_app_profileuser DE LA DB erphts_DB
    """

    date_login          = models.DateTimeField(null=True, blank=True)
    date_register       = models.DateTimeField(default = timezone.now)
    date_update         = models.DateTimeField(null=True, blank=True)
    active              = models.BooleanField(default=True)
    user                = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profusr_user')
    profile             = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profusr_Profile')
    user_register       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_register_pro")
    user_update         = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null = True, related_name = "user_update_pro")

class Activity(models.Model):
    """
    MODELO Activity REPRESENTA A LA TABLA erphts_app_activity DE LA BD erphts_DB
    Este modelo representa la actividad economica a la que se dedica la empresa
    """
    id_activity          = models.UUIDField(primary_key=True, unique = True, default = make_id_model, editable=False)
    description          = models.CharField(max_length=100)
    date_register       = models.DateTimeField(default = timezone.now)
    date_update         = models.DateTimeField(null = True, blank = True)
    user_register       = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True)
    user_update         = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, related_name = 'user_profile_act')
    active              = models.BooleanField(default=True)


    def __str__(self):
        return '%s %s' % (self.description, self.id_activity)

class BusinessLine(models.Model):
    """
    MODELO CommercialLine REPRESENTA A LA TABLA erphts_app_commercialline DE LA BD erphts_DB
    Este modelo representa el tipo de producto que se comercializa
    """
    id_busi_line        = models.UUIDField(primary_key=True, unique= True, default = make_id_model, editable = False)
    description         = models.CharField(max_length=100)
    date_register       = models.DateTimeField(default= timezone.now)
    date_update         = models.DateTimeField(null = True, blank = True)
    user_register       = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True)
    user_update         = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, related_name = 'user_profile_busiline')
    activity            = models.ForeignKey(Activity, on_delete = models.CASCADE, null = True, related_name = "acty_busiLine")
    active              = models.BooleanField(default=True)

    def __srt___(self):
        return '%s %s' % (self.description, self.id_com_line)

class TypeContributor(models.Model):
    """
    MODELO TYPECONTRIBUTOR REPRESENTA A LA TABLA erphts_app_typecontributor DE LA BD erphts_DB
    """
    id_type_contributor         = models.UUIDField(primary_key=True, unique=True, default=make_id_model, editable=False)
    description                 = models.CharField(max_length=100)
    date_register               = models.DateTimeField(default=timezone.now)
    date_update                 = models.DateTimeField(null=True, blank=True)
    user_register               = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True)
    user_update                 = models.ForeignKey(UserProfile, on_delete= models.CASCADE, null = True, related_name= "user_update_typecon")
    active                      = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s' % (self.description, self.id_type_contributor)



class Enterprise(models.Model):
    """
    MODELO ENTERPRISE REPRESENTA A LA TABLA erphts_app_ENTERPRISE DE LA BD erphts_DB
    """
    id_enterprise               = models.UUIDField(primary_key=True, unique=True, default=make_id_model, editable=False)
    email                       = models.EmailField(max_length=100, unique=True)
    ruc                         = models.CharField(max_length=13, null = True)
    name                        = models.CharField(max_length=100)
    legal_agent                 = models.CharField(max_length=50, null = True)
    telephone                   = models.CharField(max_length=10, null = True)
    telephone_fax               = models.CharField(max_length=10, null = True)
    movil_phone                 = models.CharField(max_length=10, null = True)
    address                     = models.CharField(max_length=70, null = True)
    neighborhood                = models.CharField(max_length=70, null = True)
    postal_code                 = models.CharField(max_length=10, null = True)
    web_site                    = models.CharField(max_length=200, null = True)
    date_register               = models.DateTimeField(default=timezone.now)
    date_update                 = models.DateTimeField(null=True, blank=True)
    active                      = models.BooleanField(default = True)
    user_register               = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    user_update                 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="user_update_comp")
    central_ent                 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="enterprise")
    busi_line                   = models.ForeignKey(BusinessLine, on_delete=models.CASCADE, null=True, related_name="enterprise_busiline")
    type_contrib                = models.ForeignKey(TypeContributor, on_delete=models.CASCADE, null = True, related_name = "enterprise_typeCon")

    def __str__(self):
        return self.name

