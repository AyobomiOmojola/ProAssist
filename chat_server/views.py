from django.shortcuts import render
from django.contrib.auth import get_user_model
from chat_server.models import ChatBody
from django.views import View
from urllib.parse import parse_qs
from rest_framework.authtoken.models import Token

# Create your views here.

User = get_user_model()


class ChatView(View):
    def get(self, request, username):

        token_key = parse_qs(request.scope["query_string"].decode("utf8"))["token"][0]
        token = Token.objects.get(key=token_key)
        self.user = token.user

        user_obj = User.objects.get(username=username)
        # users = User.objects.exclude(username=request.user.username)

        if self.user.id > user_obj.id:
            thread_name = f'chat_{self.user.id}-{user_obj.id}'
        else:
            thread_name = f'chat_{user_obj.id}-{self.user.id}'
        message_objs = ChatBody.objects.filter(thread_name=thread_name)

        if self.user:
            return render(request, 'chat_page.html', context={
                'user': user_obj,
                # 'users': users,
                'messages': message_objs,
                'me': self.user})
