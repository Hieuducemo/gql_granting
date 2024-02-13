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

@strawberryA.federation.type(keys=["id"], description="P, C, LC, S, ...")
class AcLessonTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        if isinstance(id, str):
            id = uuid.UUID(id)
        loader = getLoaders(info).lessontypes
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
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Finds a lesson type by its id""")
async def aclesson_type_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union["AcLessonTypeGQLModel", None]:
        result = await AcLessonTypeGQLModel.resolve_reference(info, id)
        return result

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs
LessonWhereFilter = Annotated["LessonWhereFilter",strawberryA.lazy(".AcLessonGQLModel")]
@createInputs 
@dataclass 
class LessonTypeWhereFilter: 
     name : str 
     name_en : str 
     createdby : uuid.UUID 
     
    #  lessons : LessonWhereFilter 
     
@strawberryA.field(description="""Gets all lesson types""")
async def aclesson_type_page(
        self, info: strawberryA.types.Info
    ) -> List["AcLessonTypeGQLModel"]:
        loader = getLoaders(info).lessontypes
        rows = await loader.execute_select(loader.getSelectStatement())
        return rows

