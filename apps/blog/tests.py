from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import json

from apps.blog.models import Post


class UserTestCase(TestCase):
    PASSWORD = "strongpass1"

    def setUp(self):
        author_user = get_user_model().objects.create(
            email="author@mial.com"
        )
        author_user.set_password(self.PASSWORD)
        author_user.save()

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"email": "author@mial.com", "password": self.PASSWORD},
            format="json",
        )
        self.author_user_token = json.loads(response.content)["token"]

        self.publish_post = Post.objects.create(
            title="Publish post title",
            description="Text description",
            user=author_user,
        )

    def test_get_publish_post(self):
        client = APIClient()

        response = client.get("/api/posts/{}/".format(self.publish_post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)["title"], "Publish post title")

    def test_create_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.author_user_token)

        response = client.post(
            "/api/posts/", {"title": "Create post", "description": "Post description."}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_as_anonim(self):
        client = APIClient()

        response = client.post(
            "/api/posts/", {"title": "Create post", "description": "Post description."}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
