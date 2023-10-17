import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proassist.settings")
from django.core.asgi import get_asgi_application
django.setup()
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chat_server.middlewares import TokenAuthMiddleWare
import chat_server.routing


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleWare(URLRouter(chat_server.routing.websocket_urlpatterns)),
    }
)