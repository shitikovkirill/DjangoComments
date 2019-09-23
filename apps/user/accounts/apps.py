from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "apps.user.accounts"

    def ready(self):
        import apps.user.accounts.signals  # noqa: F401
