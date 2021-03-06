from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt import views as jwtViews
from django.conf import settings

api_patterns = (
    [
        path("token/", jwtViews.obtain_jwt_token),
        path("token-refresh/", jwtViews.refresh_jwt_token),
        path("token-verify/", jwtViews.verify_jwt_token),
        path("", include("apps.user.authorisation.urls")),
        path("", include("apps.blog.urls")),
    ],
    "api",
)

urlpatterns = [path("", admin.site.urls), path("api/", include(api_patterns))]

if "rest_framework_swagger" in settings.INSTALLED_APPS:
    from rest_framework_swagger.views import get_swagger_view

    urlpatterns += [path("docs/", get_swagger_view(title="API sandbox"))]
