from api.graphql.mutations import Mutation
from api.graphql.querys import Query
import graphene

class Query(Query, graphene.ObjectType):
    pass

class Mutation(Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)