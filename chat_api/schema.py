from api.graphql.mutations import Mutation
from api.graphql.querys import Query
from api.graphql.subscriptions import Subscription
import graphene

class Query(Query, graphene.ObjectType):
    pass

class Mutation(Mutation, graphene.ObjectType):
    pass

class Subscription(Subscription):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)