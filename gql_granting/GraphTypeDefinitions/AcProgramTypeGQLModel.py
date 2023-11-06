import strawberry
import datetime
import asyncio
import strawberry as strawberryA

from typing import Annotated,Union 

from .AcProgramFormTypeGQLModel import AcProgramFormTypeGQLModel
from .AcProgramTitleTypeGQLModel import AcProgramTitleTypeGQLModel
from .AcProgramLevelTypeGQLModel import AcProgramLevelTypeGQLModel
from .AcProgramLanguageTypeGQLModel import AcProgramLanguageTypeGQLModel 

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".granting")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Encapsulation of language, level, type etc. of program. This is intermediate entity for acredited program and its types""",
)
class AcProgramTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).programtypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""english name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""datetime lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Bachelor, ...""")
    async def level(self, info: strawberryA.types.Info) -> "AcProgramLevelTypeGQLModel":
        result = await AcProgramLevelTypeGQLModel.resolve_reference(info, self.level_id)
        return result

    @strawberryA.field(description="""Present, Distant, ...""")
    async def form(self, info: strawberryA.types.Info) -> "AcProgramFormTypeGQLModel":
        result = await AcProgramFormTypeGQLModel.resolve_reference(info, self.form_id)
        return result

    @strawberryA.field(description="""Czech, ...""")
    async def language(
        self, info: strawberryA.types.Info
    ) -> "AcProgramLanguageTypeGQLModel":
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, self.language_id)
        return result

    @strawberryA.field(description="""Bc., Ing., ...""")
    async def title(self, info: strawberryA.types.Info) -> "AcProgramTitleTypeGQLModel":
        result = await AcProgramTitleTypeGQLModel.resolve_reference(info, self.title_id)
        return result

#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Finds a program type its id""")
async def program_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramTypeGQLModel", None]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, id)
        return result

#################################################
#
# Special fields for mutation
#
#################################################