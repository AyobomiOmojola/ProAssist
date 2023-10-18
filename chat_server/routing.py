from django.urls import path, re_path
from . import consumers

# Websocket routing for production:
websocket_urlpatterns = [
    re_path(r"wss/chat/(?P<id>\d+)/$", consumers.OnetoOneChatConsumer.as_asgi()),
]

# Websocket routing for development:
# websocket_urlpatterns = [
#     re_path(r"ws/chat/(?P<id>\d+)/$", consumers.OnetoOneChatConsumer.as_asgi()),
# ]