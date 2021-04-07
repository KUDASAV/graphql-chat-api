from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import authenticate
from api.graphql.types import *
from api.models import *
import graphene


class register(graphene.Mutation):
    user = graphene.Field(userType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        username = username.lower()

        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile = Profile(user=user)
        profile.save()

        #grab the jwt token from graphql_jwt
        token = get_token(user)
        return register(user=user, token=token)

class login(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(userType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        username = username.lower()
        user = authenticate(username=username, password=password)

        if user is None:
            raise Exception('Please enter valid credentials')

        token = get_token(user)
        return login(user=user, token=token)

class create_conversation(graphene.Mutation):
    conversation = graphene.Field(conversationType)

    class Arguments:
        name = graphene.String(required=True)
        members = graphene.List(graphene.Int, required=True)

    def mutate(self, info, name, members):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Authenticaticated')

        # add the user to the members
        if user.id not in members:
            members.append(user.id)

        # check if all users exist
        users = []
        for member in members:
            users.append(get_object_or_404(get_user_model(), id=member))

        conversation = Conversation(name=name)
        conversation.save()

        conversation.members.add(*users)
        conversation.save()

        return create_conversation(conversation=conversation)

class leave_conversation(graphene.Mutation):
    # remove a user from a conversation
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Authenticaticated')

        conversation = get_object_or_404(Conversation, id=id)
        conversation.members.remove(user)

        return leave_conversation(success=True)

class create_message(graphene.Mutation):
    message = graphene.Field(messageType)

    class Arguments:
        conversation = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, conversation, content):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Authenticaticated')

        conversation = get_object_or_404(Conversation, id=conversation)

        message = Message(
            author=user,
            conversation=conversation,
            content=content
        )

        message.save()
        return create_message(message=message)

class delete_message(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Authenticaticated')

        message = get_object_or_404(Message, id=id)

        # check if the user created the message
        if message.author.id != user.id:
            raise Exception('Action not allowed')

        message.delete()
        return delete_message(success=True)
        
class Mutation(graphene.ObjectType):
    login = login.Field()
    register = register.Field()

    create_conversation = create_conversation.Field()
    leave_conversation = leave_conversation.Field()

    create_message = create_message.Field()
    delete_message = delete_message.Field()