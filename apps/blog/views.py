from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from apps.blog.access_policy import PostAccessPolicy
from apps.blog.serializers import PostSerializer, AttachmentSerializer
from apps.blog.models import Post, Attachment


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostAccessPolicy]

    def create(self, request):
        post = Post.objects.create(**request.data, user=request.user)
        post.save()
        serializer_context = {"request": request}
        serializer = PostSerializer(post, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttachmentViewSet(viewsets.ModelViewSet):

    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [PostAccessPolicy]
    parser_classes = (MultiPartParser, FormParser)
