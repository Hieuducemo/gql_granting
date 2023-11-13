
import datetime
import asyncio
import strawberry as strawberryA

from typing import Optional, List, Union, Annotated
#from .AcSubjectGQLModel import AcSubjectGQLModel
#from .AcProgramTypeGQLModel import AcProgramTypeGQLModel
from .AcProgramEditorGQLModel import AcProgramEditorGQLModel
#from .externals import GroupGQLModel,UserGQLModel

def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".external")]
AcSubjectGQLModel = Annotated["AcSubjectGQLModel",strawberryA.lazy(".AcSubjectGQLModel")]
AcProgramTypeGQLModel = Annotated["AcProgramTypeGQLModel",strawberryA.lazy(".AcProgramTypeGQLModel")]
GroupGQLModel= Annotated["GroupGQLModel",strawberryA.lazy(".external")]

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing acredited study programs"""
)
class AcProgramGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).programs
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

    @strawberryA.field(description="""name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Bachelor, ...""")
    async def type(self, info: strawberryA.types.Info) -> "AcProgramTypeGQLModel":
        result = await AcProgramTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberryA.field(description="""""")
    def editor(self) -> "AcProgramEditorGQLModel":
        return self

    @strawberryA.field(description="""subjects in the program""")
    async def subjects(self, info: strawberryA.types.Info) -> List["AcSubjectGQLModel"]:
        loader = getLoaders(info).subjects
        result = await loader.filter_by(program_id=self.id)
        return result

    @strawberryA.field(description="""subjects in the program""")
    async def students(self, info: strawberryA.types.Info) -> List["UserGQLModel"]:
        loader = getLoaders(info).programstudents
        rows = await loader.filter_by(program_id=self.id)
        userawaitables = (UserGQLModel.resolve_reference(row.student_id) for row in rows)
        result = await asyncio.gather(*userawaitables)
        return result

    @strawberryA.field(description="""group defining grants of this program""")
    async def grants(self, info: strawberryA.types.Info) -> Optional["GroupGQLModel"]:
        loader = getLoaders(info).programgroups
        rows = await loader.filter_by(program_id=self.id)
        result = next(rows, None)
        return result

#################################################
#
# Special fields for query
#
#################################################

from typing import Any, NewType

JSON = strawberryA.scalar(
    NewType("JSON", object),
    description="The `JSON` scalar type represents JSON values as specified by ECMA-404",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)


@strawberryA.field(description="""Finds an program by their id""")
async def program_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramGQLModel", None]:
        result = await AcProgramGQLModel.resolve_reference(info, id)
        return result

@strawberryA.field(description="""Finds all programs""")
async def program_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List["AcProgramGQLModel"]:
        loader = getLoaders(info).programs
        result = await loader.page(skip=skip, limit=limit)
        return result
    
#################################################
#
# Special fields for mutation
#
#################################################
from typing import Optional

@strawberryA.input(description="Define input for the program" )
class ProgramInsertGQLModel:
    name: str
    type_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    pass

@strawberryA.input
class ProgramUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[strawberryA.ID] = None

@strawberryA.type
class ProgramResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def program(self, info: strawberryA.types.Info) -> Union[AcProgramGQLModel, None]:
        result = await AcProgramGQLModel.resolve_reference(info, self.id)
        return result


@strawberryA.mutation(description="""Adds new study program""")
async def program_insert(self, info: strawberryA.types.Info, program: ProgramInsertGQLModel) -> ProgramResultGQLModel:
        loader = getLoaders(info).programs
        row = await loader.insert(program)
        result = ProgramResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Update thestudy program""")
async def program_update(self, info: strawberryA.types.Info, program: ProgramUpdateGQLModel) -> ProgramResultGQLModel:
        loader = getLoaders(info).programs
        row = await loader.update(program)
        result = ProgramResultGQLModel()
        result.msg = "ok"
        result.id = program.id
        if row is None:
            result.msg = "fail"
            
        return result

    
