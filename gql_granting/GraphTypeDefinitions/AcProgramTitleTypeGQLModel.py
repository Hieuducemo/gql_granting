import strawberry
import datetime
import asyncio
import strawberry as strawberryA
import uuid
from typing import Optional, List, Union, Annotated

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

#UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".granting")]

@strawberryA.federation.type(keys=["id"], description="Bc., Ing., ...")
class AcProgramTitleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoaders(info).programtitletypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberryA.field(description="primary key")
    def id(self) -> uuid.UUID:
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
@strawberryA.field(description="""Finds a program title by its id""")
async def program_title_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union["AcProgramTitleTypeGQLModel", None]:
        result = await AcProgramTitleTypeGQLModel.resolve_reference(info, id)
        return result


