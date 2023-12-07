import strawberry
import datetime
import asyncio
import strawberry as strawberryA
from uuid import UUID 
from typing import Optional, List, Union, Annotated

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

#UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".granting")]

@strawberryA.federation.type(
    keys=["id"], description="Classification at the end of semester"
)
class AcClassificationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: UUID):
        loader = getLoaders(info).classificationtypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="primary key")
    def id(self) -> UUID:
        return self.id

    @strawberryA.field(description="name")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="english name")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="datetime lastchange")
    def lastchange(self) -> str:
        return self.lastchange
    
#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Lists classifications types""")
async def acclassification_type_page(
        self, info: strawberryA.types.Info, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> List["AcClassificationTypeGQLModel"]:
        loader = getLoaders(info).classificationtypes
        result = await loader.page(skip, limit)
        return result

