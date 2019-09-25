from django.urls import include, path
from rest_framework import routers
from apps.blog.views import PostViewSet, AttachmentViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"files", AttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
