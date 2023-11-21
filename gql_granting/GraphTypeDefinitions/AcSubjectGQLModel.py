
import datetime
import strawberry as strawberryA

from typing import Optional, List, Annotated
from .externals import GroupGQLModel 
#from .AcProgramGQLModel import AcProgramGQLModel
from .AcSemesterGQLModel import AcSemesterGQLModel


from typing import Optional, List, Union, Annotated
import strawberry as strawberryA
def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

#UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".granting")]

AcProgramGQLModel = Annotated["AcProgramGQLModel",strawberryA.lazy(".AcProgramGQLModel")]
AcSemesterGQLModel =Annotated["AcSemesterGQLModel",strawberryA.lazy(".AcSemesterGQLModel")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which connects programs and semesters, includes informations about subjects (divided into semesters)""",
)
class AcSubjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).subjects
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""english name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""datetime laschange""")
    def lastchange(self) -> str:
        return self.lastchange

    @strawberryA.field(description="""Program owing this subjects""")
    async def program(self, info: strawberryA.types.Info) -> Optional["AcProgramGQLModel"]:
        from .AcProgramGQLModel import AcProgramGQLModel
        result = await AcProgramGQLModel.resolve_reference(info, self.program_id)
        return result

    @strawberryA.field(description="""Semesters which the subjects in divided into""")
    async def semesters(
        self, info: strawberryA.types.Info
    ) -> List["AcSemesterGQLModel"]:
        loader = getLoaders(info).semesters
        result = await loader.filter_by(subject_id=self.id)
        return result

    @strawberryA.field(description="""group defining grants of this subject""")
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

@strawberryA.field(description="""Finds a subject by its id""")
async def acsubject_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcSubjectGQLModel", None]:
        result = await AcSubjectGQLModel.resolve_reference(info, id)
        return result

@strawberryA.field(description="""Finds a subject by its id""")
async def acsubject_page(
        self, info: strawberryA.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
    ) -> Union["AcSubjectGQLModel", None]:
        loader = getLoaders(info).subjects
        result = await loader.page()
        result = await AcSubjectGQLModel.resolve_reference(info, id)
        return result
    
#################################################
#
# Special fields for mutation
#
#################################################

@strawberryA.input
class SubjectInsertGQLModel:
    name: str
    name_en: str
    program_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = True

@strawberryA.input
class SubjectUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    valid: Optional[bool] = None

@strawberryA.type
class SubjectResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of subject operation""")
    async def subject(self, info: strawberryA.types.Info) -> Union[AcSubjectGQLModel, None]:
        result = await AcSubjectGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.mutation(description="""Adds a new study subject""")
async def subject_insert(self, info: strawberryA.types.Info, subject: SubjectInsertGQLModel) -> SubjectResultGQLModel:
        loader = getLoaders(info).subjects
        row = await loader.insert(subject)
        result = SubjectResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Update the study subject""")
async def subject_update(self, info: strawberryA.types.Info, subject: SubjectUpdateGQLModel) -> SubjectResultGQLModel:
        loader = getLoaders(info).subjects
        row = await loader.update(subject)
        result = SubjectResultGQLModel()
        result.msg = "ok"
        result.id = subject.id
        if row is None:
            result.msg = "fail"
            
        return result