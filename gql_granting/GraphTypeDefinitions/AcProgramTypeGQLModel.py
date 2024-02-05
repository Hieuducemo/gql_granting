
import datetime
import strawberry as strawberryA
from typing import Union, Optional,Annotated
#from .AcProgramGQLModel import ProgramUpdateGQLModel
from .AcProgramFormTypeGQLModel import AcProgramFormTypeGQLModel
from .AcProgramTitleTypeGQLModel import AcProgramTitleTypeGQLModel
from .AcProgramLevelTypeGQLModel import AcProgramLevelTypeGQLModel
from .AcProgramLanguageTypeGQLModel import AcProgramLanguageTypeGQLModel 
import uuid 

def getLoaders(info):    
    return info.context['all']
# def getUser(info):
#     return info.context["user"]

ProgramUpdateGQLModel= Annotated["ProgramUpdateGQLModel",strawberryA.lazy(".AcProgramGQLModel")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Encapsulation of language, level, type etc. of program. This is intermediate entity for acredited program and its types""",
)
class AcProgramTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        loader = getLoaders(info).programtypes
        if isinstance(id, str): id = uuid.UUID(id)
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> uuid.UUID:
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
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union["AcProgramTypeGQLModel", None]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, id)
        return result
    
from dataclasses import dataclass
from uoishelpers.resolvers import createInputs

# ProgramWhereFilter = Annotated["ProgramWhereFilter", strawberryA.lazy(".AcProgramGQLModel")]
@createInputs
@dataclass 
class ProgramTypeWhereFilter: 
    name: str   
    name_en: str 
    id: uuid.UUID 
    
    #programs: ProgramWhereFilter 
    
#################################################
#
# Special fields for mutation
#
#################################################

@strawberryA.input(description="Insert new program type")
class ProgramTypeInsertGQLModel:
    name: str
    name_en: str
    language_id: uuid.UUID
    level_id: uuid.UUID
    form_id: uuid.UUID
    title_id: uuid.UUID
    id: Optional[uuid.UUID] = None
    pass


@strawberryA.input(description="Update current study program type")
class ProgramTypeUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    language_id: Optional[uuid.UUID] = None
    level_id: Optional[uuid.UUID] = None
    form_id: Optional[uuid.UUID] = None
    title_id: Optional[uuid.UUID] = None
    
@strawberryA.type
class ProgramTypeResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def program_type(self, info: strawberryA.types.Info) -> Union[AcProgramTypeGQLModel, None]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="""Adds a new study program type""")
async def program_type_insert(self, info: strawberryA.types.Info, program_type: ProgramTypeInsertGQLModel) -> ProgramTypeResultGQLModel:
        loader = getLoaders(info).programtypes
        row = await loader.insert(program_type)
        result = ProgramTypeResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result
    
@strawberryA.mutation(description="""Update the study program type""")
async def program_type_update(self, info: strawberryA.types.Info, program_type: ProgramTypeUpdateGQLModel) -> ProgramTypeResultGQLModel:
        loader = getLoaders(info).programtypes
        row = await loader.update(program_type)
        result = ProgramTypeResultGQLModel()
        result.msg = "ok"
        result.id = program_type.id
        # if row is None:
        #     result.msg = "fail"
             
        return result
    