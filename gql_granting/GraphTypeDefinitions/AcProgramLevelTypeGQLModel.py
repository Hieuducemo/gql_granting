import strawberry
import datetime
import asyncio
import strawberry as strawberryA
import uuid

from typing import Optional, List, Union, Annotated

def getLoaders(info):
    return info.context['all']
# def getUser(info):
#     return info.context["user"] 

#UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".granting")]

@strawberryA.federation.type(keys=["id"], description="bachelor, ...")
class AcProgramLevelTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        if isinstance(id, str):
             id = uuid.UUID(id)
        loader = getLoaders(info).programleveltypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberryA.field(description="primary key")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberryA.field(description="Name of the program level")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="name in english")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

#################################################
#
# Special fields for query
#
#################################################
@strawberryA.field(description="""Finds a program level its id""")
async def program_level_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union["AcProgramLevelTypeGQLModel", None]:
        result = await AcProgramLevelTypeGQLModel.resolve_reference(info, id)
        return result

