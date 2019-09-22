from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import json


class UserTestCase(TestCase):
    password = "strongpass1"
    email = "user1@mial.com"

    def setUp(self):
        user = get_user_model().objects.create(email=self.email)
        user.set_password(self.password)
        user.save()

        client = APIClient()
        response = client.post(
            "/api/token/",
            {"email": self.email, "password": self.password},
            format="json",
        )
        self.test_user_token = json.loads(response.content)["token"]

    def test_register_user(self):
        client = APIClient()
        response = client.post(
            "/api/users/", {"email": "test_user@mial.com", "password": "strongpass1"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)["email"], "test_user@mial.com")

    def test_register_user_fail_email(self):
        client = APIClient()
        response = client.post(
            "/api/users/", {"email": "test_usermial.com", "password": "strongpass1"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Enter a valid email address.", json.loads(response.content)["email"]
        )

    def test_register_user_fail_no_data(self):
        client = APIClient()
        response = client.post("/api/users/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", json.loads(response.content)["email"])
        self.assertIn(
            "This field is required.", json.loads(response.content)["password"]
        )

    def test_register_user_with_authenticated_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + self.test_user_token)
        response = client.post(
            "/api/users/",
            {
                "username": "test_user2",
                "email": "test_user2@mial.com",
                "password": "strongpass1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content)["detail"],
            "You do not have permission to perform this action.",
        )

    def test_token(self):
        client = APIClient()
        response = client.post(
            "/api/token/",
            {"email": self.email, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)["token"])

    def test_token_fail(self):
        client = APIClient()
        response = client.post(
            "/api/token/",
            {"email": "user_not_in_db@mail.com", "password": "strongpass1"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(json.loads(response.content)["non_field_errors"])
        self.assertIn(
            "Unable to log in with provided credentials.",
            json.loads(response.content)["non_field_errors"],
        )

    def test_token_refresh(self):

        client = APIClient()
        response = client.post(
            "/api/token-refresh/", {"token": self.test_user_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)["token"])

    def test_token_refresh_fail(self):
        client = APIClient()
        response = client.post(
            "/api/token-refresh/", {"token": "Wrong token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(json.loads(response.content)["non_field_errors"])
        self.assertIn(
            "Error decoding token.", json.loads(response.content)["non_field_errors"]
        )

    def test_token_verify(self):
        client = APIClient()
        response = client.post(
            "/api/token-verify/", {"token": self.test_user_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)["token"])
        self.assertEquals(self.test_user_token, json.loads(response.content)["token"])

    def test_token_verify_fail(self):
        client = APIClient()
        response = client.post(
            "/api/token-verify/", {"token": "Wrong token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(json.loads(response.content)["non_field_errors"])
        self.assertIn(
            "Error decoding token.", json.loads(response.content)["non_field_errors"]
        )
