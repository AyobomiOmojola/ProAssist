import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proassist.settings")
from django.core.asgi import get_asgi_application
django.setup()
django_asgi_app = get_asgi_application()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path



from chat_server.middlewares import TokenAuthMiddleWare
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.


from chat_server import consumers
import chat_server.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleWare(URLRouter(chat_server.routing.websocket_urlpatterns)),
    }
)