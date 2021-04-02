from django.contrib.auth import get_user_model
from api.graphql.pagination import get_paginator
from django.shortcuts import get_object_or_404
from api.graphql.types import *
from api.models import *
import graphene

class Query(object):
    user = graphene.Field(userType)
    user_search = graphene.Field(usersList, username = graphene.String(required=True), page=graphene.Int(), limit=graphene.Int())
    conversations = graphene.Field(conversationsList, page=graphene.Int(), limit=graphene.Int())
    messages = graphene.Field(messagesList, conversation=graphene.Int(required=True), page=graphene.Int(), limit=graphene.Int())

    def resolve_user(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Not Authenticaticated')

        return user

    def resolve_user_search(self, info, username, page=1, limit=10):
        users = get_user_model().objects.all()

        if info.context.user.is_anonymous:
            raise Exception('Not Authenticaticated')

        return get_paginator(users, usersList, page=page, limit=limit)

    def resolve_conversations(self, info, page=1, limit=10):
        user = info.context.user
       
        if user.is_anonymous:
            raise Exception('Not Authenticaticated')
        
        conversations = user.conversation_set.all()
        return get_paginator(conversations, conversationsList, page=page, limit=limit)

    def resolve_messages(self, info, conversation, page=1, limit=10):
        user = info.context.user
       
        if user.is_anonymous:
            raise Exception('Not Authenticaticated')
        
        conversation = get_object_or_404(Conversation, id=conversation)

        if user not in conversation.members.all():
            raise Exception('User not in conversation')

        messages = conversation.message_set.all()
        return get_paginator(messages, messagesList, page=page, limit=limit)
