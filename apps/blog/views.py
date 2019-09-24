from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.blog.access_policy import PostAccessPolicy
from apps.blog.serializers import PostSerializer
from apps.blog.permissions import IsOwner
from apps.blog.models import Post


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostAccessPolicy]

    def create(self, request):
        composition = Post.objects.create(**request.data, user=request.user)
        composition.save()
        serializer_context = {"request": request}
        serializer = PostSerializer(composition, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)