import datetime
import asyncio
import strawberry as strawberryA
import typing
from uuid import UUID
from typing import Optional, List, Union, Annotated
from .externals import UserGQLModel
def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]


class AcProgramStudentGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).programstudents
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result
    
    @strawberryA.field(description="""primary key""")
    async def user(self, info: strawberryA.types.Info) -> Optional["UserGQLModel"]:
        return await UserGQLModel.resolve_reference(id=self.student_id)
    
    @strawberryA.field(description="""primary key""")
    async def messages(self, info: strawberryA.types.Info) -> Optional["UserGQLModel"]:
        return await UserGQLModel.resolve_reference(id=self.student_id)