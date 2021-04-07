from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.urls import path 
from graphql_jwt.utils import jwt_decode
from django.contrib.auth import get_user_model
User = get_user_model()

@database_sync_to_async
def get_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return AnonymousUser()

class QueryAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return QueryAuthMiddlewareInstance(scope, self)

class QueryAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        # Not authenticated by default
        user_object = AnonymousUser()

        headers = dict(self.scope['headers'])

        if b'authorization' in headers:
            jwt_token = headers[b'authorization'].decode().lstrip('JWT ')
            
            # decode token and get user object
            user = jwt_decode(jwt_token)
            user_object = await get_user(user['username'])
           
        self.scope['user'] = user_object
        inner = self.inner(self.scope)
        return await inner(receive, send)

application = ProtocolTypeRouter({
    "websocket": QueryAuthMiddleware(
        URLRouter([
            path('', GraphqlSubscriptionConsumer)
        ])
    ),
})