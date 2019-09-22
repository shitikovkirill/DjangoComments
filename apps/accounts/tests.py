from django.test import TestCase
from unittest.mock import MagicMock

from apps.accounts.models import MyUserManager


class AccountsTestCase(TestCase):
    def test_create_user(self):
        user = MagicMock()
        email = "test@mail.com"
        password = "test"

        user_manager = MyUserManager()
        user_manager.model = MagicMock(return_value=user)
        created_user = user_manager.create_user(email, password)

        user_manager.model.assert_called_once_with(
            email=email, is_staff=False, is_superuser=False
        )
        user.set_password.assert_called_once_with(password)
        user.save.assert_called_once()
        self.assertIs(created_user, user)

    def test_create_super_user(self):
        user = MagicMock()
        email = "test@mail.com"
        password = "test"

        user_manager = MyUserManager()
        user_manager.model = MagicMock(return_value=user)
        created_user = user_manager.create_superuser(email, password)

        user_manager.model.assert_called_once_with(
            email=email, is_active=True, is_staff=True, is_superuser=True
        )
        user.set_password.assert_called_once_with(password)
        user.save.assert_called_once()
        self.assertIs(created_user, user)
