import strawberry
import datetime
import asyncio
import strawberry as strawberryA

from typing import Optional, List, Union, Annotated
#from .AcSemesterGQLModel import AcSemesterGQLModel
from .AcClassificationLevelGQLModel import AcClassificationLevelGQLModel


def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".externals")]
AcSemesterGQLModel= Annotated["AcSemesterGQLModel",strawberryA.lazy(".AcSemesterGQLModel")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which holds a exam result for a subject semester and user / student""",
)
class AcClassificationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).classifications
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""datetime lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""datetime of classification""")
    def date(self) -> datetime.datetime:
        return self.date

    @strawberryA.field(description="""ORDER OF CLASSI""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""User""")
    async def user(self, info: strawberryA.types.Info) -> Optional["UserGQLModel"]:
        return await UserGQLModel.resolve_reference(id=self.user_id)

    @strawberryA.field(description="""Semester""")
    async def semester(self, info: strawberryA.types.Info) -> Optional["AcSemesterGQLModel"]:
        result = await AcSemesterGQLModel.resolve_reference(info, id=self.semester_id)
        return result

    # @strawberryA.field(description="""Type""")
    # async def type(self, info: strawberryA.types.Info) -> "AcClassificationTypeGQLModel":
    #     result = await AcClassificationTypeGQLModel.resolve_reference(info, id=self.classificationtype_id)
    #     return result

    @strawberryA.field(description="""Level""")
    async def level(self, info: strawberryA.types.Info) -> "AcClassificationLevelGQLModel":
        result = await AcClassificationLevelGQLModel.resolve_reference(info, id=self.classificationlevel_id)
        return result

#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Lists classifications""")
async def acclassification_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List["AcClassificationGQLModel"]:
        loader = getLoaders(info).classifications
        result = await loader.page(skip=skip, limit=limit)
        return result

@strawberryA.field(description="""Lists classifications for the user""")
async def acclassification_page_by_user(
        self, info: strawberryA.types.Info, user_id: strawberryA.ID, skip: int = 0, limit: int = 10
    ) -> List["AcClassificationGQLModel"]:
        loader = getLoaders(info).classifications
        result = await loader.filter_by(user_id=user_id)
        return result

#################################################
#
# Special fields for mutation
#
#################################################

@strawberryA.input
class ClassificationInsertGQLModel:
    semester_id: strawberryA.ID
    user_id: strawberryA.ID
    classificationlevel_id: strawberryA.ID
    # classificationtype_id: strawberryA.ID
    order: int
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class ClassificationUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    classificationlevel_id: strawberryA.ID

@strawberryA.type
class ClassificationResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of semester operation""")
    async def classification(self, info: strawberryA.types.Info) -> Union[AcClassificationGQLModel, None]:
        result = await AcClassificationGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.mutation(description="""Adds new classification (a mark for student)""")
async def classification_insert(self, info: strawberryA.types.Info, classification: ClassificationInsertGQLModel) -> ClassificationResultGQLModel:
        loader = getLoaders(info).classifications
        row = await loader.insert(classification)
        result = ClassificationResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Update the classification (a mark for student)""")
async def classification_update(self, info: strawberryA.types.Info, classification: ClassificationUpdateGQLModel) -> ClassificationResultGQLModel:
        loader = getLoaders(info).classifications
        row = await loader.update(classification)
        result = ClassificationResultGQLModel()
        result.msg = "ok"
        result.id = classification.id
        if row is None:
            result.msg = "fail"
            
        return result
