from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import json

from apps.blog.models import Post


class UserTestCase(TestCase):
    PASSWORD = "strongpass1"

    def setUp(self):
        author_user = get_user_model().objects.create(email="author@mial.com")
        author_user.set_password(self.PASSWORD)
        author_user.save()

        self.client = APIClient()
        response = self.client.post(
            "/api/token/",
            {"email": "author@mial.com", "password": self.PASSWORD},
            format="json",
        )
        self.author_user_token = json.loads(response.content)["token"]

        self.publish_post = Post.objects.create(
            title="Publish post title", description="Text description", user=author_user
        )

    def test_get_publish_post(self):
        response = self.client.get("/api/posts/{}/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["title"], "Publish post title")

    def test_create_post(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_user_token)

        response = self.client.post(
            "/api/posts/", {"title": "Create post", "description": "Post description."}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_as_anonim(self):
        response = self.client.post(
            "/api/posts/", {"title": "Create post", "description": "Post description."}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_files(self):
        _io = StringIO()
        _io.write("foo")
        file = InMemoryUploadedFile(_io, None, "foo.txt", "text", 0, None)
        file.seek(0)

        data = {"file": file, "post": self.publish_post.id}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_user_token)
        response = self.client.post("/api/files/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, len(self.publish_post.attachments.all()))

        _io = StringIO()
        _io.write("foo2")
        file = InMemoryUploadedFile(_io, None, "foo2.txt", "text", 0, None)
        file.seek(0)

        data = {"file": file, "post": self.publish_post.id}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_user_token)
        response = self.client.post("/api/files/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, len(self.publish_post.attachments.all()))
