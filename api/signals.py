from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription
from django.db.models.signals import post_save, post_delete
from api.models import *

# new conversation created
post_save.connect(post_save_subscription, sender=Conversation, dispatch_uid="actions_save")

# new message recieved
post_save.connect(post_save_subscription, sender=Message, dispatch_uid="actions_save")