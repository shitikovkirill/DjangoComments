from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from apps.user.authorisation.access_policy import UserAccessPolicy
from .serializers import UserSerializer, GroupSerializer, TokenSerializer
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [UserAccessPolicy]

    @action(methods=['post'], detail=True, url_path='confirm-email')
    def confirm_email(self, request, pk):
        user = get_object_or_404(get_user_model(), id=pk)
        token_ser = TokenSerializer(user=user, data=request.data)
        token_ser.is_valid(raise_exception=True)
        user.email_confirmed = True
        user.save()
        return Response({"detail": "Email confirmed"})


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)
