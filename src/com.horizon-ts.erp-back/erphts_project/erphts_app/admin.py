from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Person)
admin.site.register(models.Profile)
admin.site.register(models.ProfileUser)
admin.site.register(models.Province)
admin.site.register(models.Canton)
admin.site.register(models.Parish)
admin.site.register(models.Enterprise)
admin.site.register(models.Activity)
admin.site.register(models.BusinessLine)
admin.site.register(models.TypeContributor)
