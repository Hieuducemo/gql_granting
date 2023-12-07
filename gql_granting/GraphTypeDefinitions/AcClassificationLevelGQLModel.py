
import strawberry as strawberryA
from uuid import UUID
from typing import  Annotated


def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

#UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".granting")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Mark which student could get as an exam evaluation""",
)
class AcClassificationLevelGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: UUID):
        loader = getLoaders(info).classificationlevels
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> UUID:
        return self.id

    @strawberryA.field(description="""name (like A)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""name (like A)""")
    def name_en(self) -> str:
        return self.name_en
    
