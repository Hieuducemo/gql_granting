import strawberry
import datetime
import asyncio
import strawberry as strawberryA
import uuid
from typing import Optional, List, Union, Annotated
import typing
def getLoaders(info):
    return info.context['all']
# def getUser(info):
#     return info.context["user"]

UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".externals")]


@strawberryA.federation.type(
    keys=["id"], description="Classification at the end of semester"
)
class AcClassificationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoaders(info).classificationtypes
        if isinstance(id, str): id = uuid.UUID(id)
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberryA.field(description="primary key")
    def id(self) -> uuid.UUID:
        return self.id
    
    # @strawberryA.field(description="""User""")
    # async def user(self, info: strawberryA.types.Info) -> Optional["UserGQLModel"]:
    #     from .externals import UserGQLModel
    #     return await UserGQLModel.resolve_reference(id=self.user_id) 
    
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

@strawberryA.field(description="""Lists classifications types""")
async def acclassification_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List["AcClassificationTypeGQLModel"]:
        loader = getLoaders(info).classificationtypes
        result = await loader.page(skip, limit)
        return result

@strawberryA.field(description="""Finds a classification type its id""")
async def classification_type_by_id(
         self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union["AcClassificationTypeGQLModel", None]:
        result = await AcClassificationTypeGQLModel.resolve_reference(info, id)
        return result 

from dataclasses import dataclass 
from uoishelpers.resolvers import createInputs 
ClassificationWhereFilter = Annotated["ClassificationWhereFilter", strawberryA.lazy(".AcClassificationGQLModel")]

@createInputs
@dataclass 
class ClassificationTypeWhereFilter: 
    name : str 
    name_en : str 
    createdby :uuid.UUID 
    
    # classifications: ClassificationWhereFilter 
