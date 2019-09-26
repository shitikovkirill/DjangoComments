from django.urls import include, path
from rest_framework import routers
from apps.user.authorisation.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [path("", include(router.urls))]
