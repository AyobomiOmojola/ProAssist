from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"wss/chat/(?P<id>\d+)/$", consumers.OnetoOneChatConsumer.as_asgi()),
]