from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<id>\d+)/$", consumers.OnetoOneChatConsumer.as_asgi()),
]