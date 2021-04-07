from graphene_subscriptions.events import CREATED, DELETED, UPDATED 
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from api.graphql.types import *
from api.models import *
import graphene


class Subscription(graphene.ObjectType):
    new_conversation = graphene.Field(conversationType)
    new_message = graphene.Field(messageType)

    def resolve_new_conversation(root, info):
        user = info.context.user
        
        # we have to watch the updated event because the members ManyToMany field
        # is only updated with the related user models after creation
        event = root.filter(
            lambda event:
                event.operation == UPDATED and
                isinstance(event.instance, Conversation) and

                # check if the user is in the conversation
                event.instance.members.filter(id=user.id).exists() 
        ).map(lambda event: event.instance)

        return event

    def resolve_new_message(root, info):
        user = info.context.user
        
        event = root.filter(
            lambda event:
                event.operation == CREATED and
                isinstance(event.instance, Message) and
                
                # check if the message belongs to a conversation the user in
                event.instance.conversation in user.conversation_set.all()
        ).map(lambda event: event.instance)

        return event