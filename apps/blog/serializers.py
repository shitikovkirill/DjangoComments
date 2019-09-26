import os
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.blog.models import Post, Attachment, Comment


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "description", "user")


class AttachmentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Attachment
        fields = ("id", "file", "post", "name", "version", "upload_date", "size")
        read_only_fields = ("owner", "name", "version", "upload_date", "size")

    def validate(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        validated_data["name"] = os.path.splitext(validated_data["file"].name)[0]
        validated_data["size"] = validated_data["file"].size
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "text")
