from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from api.graphql.pagination import get_paginator
from api.models import *
import graphene

class userType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class userSearchType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

class usersList(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    count = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    result = graphene.List(userSearchType)

class messageType(DjangoObjectType):
    class Meta:
        model = Message

class messagesList(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    count = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    result = graphene.List(messageType)

class conversationType(DjangoObjectType):
    class Meta:
        model = Conversation

class conversationsList(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    count = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    result = graphene.List(conversationType)