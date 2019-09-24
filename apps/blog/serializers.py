from apps.user.authorisation.serializers import UserSerializer
from rest_framework import serializers
from apps.blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ("id", "title", "description", "user", "file")
