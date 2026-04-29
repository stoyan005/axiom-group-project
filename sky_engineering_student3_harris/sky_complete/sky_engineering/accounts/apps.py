
from django.apps import AppConfig


class AccountsConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Importing signals here registers the post_save handlers.
        # noqa is used because the import is for side effects, not direct use.
        import accounts.signals  # noqa: F401
