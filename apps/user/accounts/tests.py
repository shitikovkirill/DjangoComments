from django.test import TestCase
from unittest.mock import MagicMock, patch


from apps.user.accounts.models import MyUserManager


class AccountsTestCase(TestCase):
    @patch("apps.user.accounts.models.async_to_sync")
    @patch("apps.user.accounts.models.get_channel_layer")
    def test_create_user(self, async_to_sync, get_channel_layer):
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

    @patch("apps.user.accounts.models.async_to_sync")
    @patch("apps.user.accounts.models.get_channel_layer")
    def test_create_super_user(self, async_to_sync, get_channel_layer):
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
