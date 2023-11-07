import strawberry

from .query import Query
from .mutation import Mutation
from .externals import UserGQLModel,GroupGQLModel

schema = strawberry.federation.Schema(query=Query, mutation=Mutation,types=(
    UserGQLModel,GroupGQLModel
))
# schema = strawberry.federation.Schema(query=Query)