from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("login", views.LoginViewSet, base_name = "login")
router.register("UserProfile", views.UserProfileViewSet)
router.register("person", views.PersonViewSet)
router.register("Activity", views.ActivityViewSet)
router.register("BusinessLine", views.BusinessLineViewSet)
router.register("TypeContributor", views.TypeContributorViewSet)
router.register("Enterprise", views.EnterpriseViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]