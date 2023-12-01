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
    keys=["id"], description="Program form type (Present, distant, ...)"
)
class AcProgramFormTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: UUID):
        loader = getLoaders(info).programforms
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

    @strawberryA.field(description="name")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="")
    def lastchange(self) -> str:
        return self.lastchange


#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Finds a program from its id""")
async def program_form_by_id(
        self, info: strawberryA.types.Info, id: UUID
    ) -> Union["AcProgramFormTypeGQLModel", None]:
        result = await AcProgramFormTypeGQLModel.resolve_reference(info, id)
        return result


