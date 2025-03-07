
import datetime
import strawberry as strawberryA

from typing import Optional, List, Union, Annotated
#from .AcTopicGQLModel import AcTopicGQLModel
from .AcClassificationTypeGQLModel import AcClassificationTypeGQLModel
#from .AcClassificationGQLModel import AcClassificationGQLModel
import uuid 
def getLoaders(info):
    return info.context['all']
# def getUser(info):
#     return info.context["user"]

AcClassificationGQLModel= Annotated["AcClassificationGQLModel",strawberryA.lazy(".AcClassificationGQLModel")]
AcTopicGQLModel= Annotated["AcTopicGQLModel",strawberryA.lazy(".AcTopicGQLModel")]
AcSubjectGQLModel=Annotated["AcSubjectGQLModel",strawberryA.lazy(".AcSubjectGQLModel")]

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing each semester in study subject"""
)
class AcSemesterGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
        if isinstance(id, str):
             id = uuid.UUID(id)

        loader = getLoaders(info).semesters
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
    
    @strawberryA.field(description="""semester number""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""credits""")
    def credits(self) -> int:
        return self.credits

    @strawberryA.field(description="""credits""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange


    # FK###############################################################################################
    @strawberryA.field(description="""Subject related to the semester (semester owner)""")
    async def subject(self, info: strawberryA.types.Info) -> Optional["AcSubjectGQLModel"]:
        from .AcSubjectGQLModel import AcSubjectGQLModel
        result = await AcSubjectGQLModel.resolve_reference(info, self.subject_id)
        return result

    @strawberryA.field(description="""Subject related to the semester (semester owner)""")
    async def classification_type(self, info: strawberryA.types.Info) -> "AcClassificationTypeGQLModel":
        result = await AcClassificationTypeGQLModel.resolve_reference(info, self.classificationtype_id)
        return result

    @strawberryA.field(description="""Final classification of the semester""")
    async def classifications(
        self, info: strawberryA.types.Info
    ) -> List["AcClassificationGQLModel"]:
        #loader = getLoaders(info).acclassification_for_semester
        loader = getLoaders(info).classifications
        result = await loader.filter_by(semester_id=self.id)
        return result

    @strawberryA.field(description="""topics""")
    async def topics(self, info: strawberryA.types.Info) -> List["AcTopicGQLModel"]:
        loader = getLoaders(info).topics
        result = await loader.filter_by(semester_id=self.id)
        return result

#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Finds a subject semester by its id""")
async def acsemester_by_id(
        self, info: strawberryA.types.Info, id: uuid.UUID
    ) -> Union["AcSemesterGQLModel", None]:
        result = await AcSemesterGQLModel.resolve_reference(info, id)
        return result

@strawberryA.field(description="""Finds a subject semester by its id""")
async def acsemester_page(
        self, info: strawberryA.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
    ) -> List["AcSemesterGQLModel"]:
        loader = getLoaders(info).semesters
        result = await loader.page(skip=skip, limit=limit)
        return result


    
#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Finds a subject semester by its id""")
async def acsemester_page(
        self, info: strawberryA.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10
    ) -> List["AcSemesterGQLModel"]:
        loader = getLoaders(info).semesters
        result = await loader.page(skip=skip, limit=limit)
        return result

#################################################
#
# Special fields for mutation
#
#################################################

@strawberryA.input
class SemesterInsertGQLModel:
    subject_id:uuid.UUID
    classificationtype_id: uuid.UUID
    order: Optional[int] = 0
    credits: Optional[int] = 0
    id: Optional[uuid.UUID] = None
    valid: Optional[bool] = True

@strawberryA.input
class SemesterUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    order: Optional[int] = None
    credits: Optional[int] = None
    classificationtype_id: Optional[uuid.UUID] = None

@strawberryA.type
class SemesterResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberryA.field(description="""Result of semester operation""")
    async def semester(self, info: strawberryA.types.Info) -> Union[AcSemesterGQLModel, None]:
        result = await AcSemesterGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="""Adds a new semester to study program""")
async def semester_insert(self, info: strawberryA.types.Info, semester: SemesterInsertGQLModel) -> SemesterResultGQLModel:
        loader = getLoaders(info).semesters
        row = await loader.insert(semester)
        print("semester_insert", row.id, row.classificationtype_id)
        result = SemesterResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Update the semester of study program""")
async def semester_update(self, info: strawberryA.types.Info, semester: SemesterUpdateGQLModel) -> SemesterResultGQLModel:
        loader = getLoaders(info).semesters
        row = await loader.update(semester)
        result = SemesterResultGQLModel()
        result.msg = "ok"
        result.id = semester.id
        # if row is None:
        #     result.msg = "fail"
            
        return result