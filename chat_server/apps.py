from django.apps import AppConfig


class ChatServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_server'

    # def ready(self):
    #     import chat_server.signals
