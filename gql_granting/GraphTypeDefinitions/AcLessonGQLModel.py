import strawberry
import datetime
import asyncio
import strawberry as strawberryA

from typing import Optional, List, Union, Annotated
from .AcLessonTypeGQLModel import AcLessonTypeGQLModel
#from .AcTopicGQLModel import AcTopicGQLModel
def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

AcTopicGQLModel= Annotated["AcTopicGQLModel",strawberryA.lazy(".AcTopicGQLModel")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which represents single lesson included in a topic""",
)
class AcLessonGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).lessons
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

    # FK###############################################################################################
    @strawberryA.field(description="""Lesson type""")
    async def type(self, info: strawberryA.types.Info) -> "AcLessonTypeGQLModel":
        result = await AcLessonTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    ##################################################################################################
    @strawberryA.field(description="""Number of hour of this lesson in the topic""")
    def count(self) -> int:
        return self.count

    @strawberryA.field(description="""The topic which owns this lesson""")
    async def topic(self, info: strawberryA.types.Info) -> "AcTopicGQLModel":
        result = await AcTopicGQLModel.resolve_reference(info, self.topic_id)
        return result

#################################################
#
# Special fields for query
#
#################################################

@strawberryA.field(description="""Finds a lesson by its id""")
async def aclesson_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcLessonGQLModel", None]:
        result = await AcLessonGQLModel.resolve_reference(info, id)
        return result

@strawberryA.field(description="""Gets all lesson types""")
async def aclesson_type_page(
        self, info: strawberryA.types.Info
    ) -> List["AcLessonTypeGQLModel"]:
        loader = getLoaders(info).lessontypes
        rows = await loader.execute_select(loader.getSelectStatement())
        return rows
    
#################################################
#
# Special fields for mutation
#
#################################################
@strawberryA.type
class TopicResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of topic operation""")
    async def topic(self, info: strawberryA.types.Info) -> Union[AcTopicGQLModel, None]:
        result = await AcTopicGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input
class LessonInsertGQLModel:
    topic_id: strawberryA.ID
    type_id: strawberryA.ID = strawberryA.field(description="type of the lesson")
    count: Optional[int] = strawberryA.field(description="count of the lessons", default=2)
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class LessonUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    type_id: Optional[strawberryA.ID] = None
    count: Optional[int] = None

@strawberryA.type
class LessonResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of topic operation""")
    async def topic(self, info: strawberryA.types.Info) -> Union[AcLessonGQLModel, None]:
        result = await AcLessonGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.mutation(description="""Adds new study lesson""")
async def lesson_insert(self, info: strawberryA.types.Info, lesson: LessonInsertGQLModel) -> LessonResultGQLModel:
        loader = getLoaders(info).lessons
        row = await loader.insert(lesson)
        result = LessonResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Update the study lesson""")
async def lesson_update(self, info: strawberryA.types.Info, lesson: LessonUpdateGQLModel) -> TopicResultGQLModel:
        loader = getLoaders(info).lessons
        row = await loader.update(lesson)
        result = LessonResultGQLModel()
        result.msg = "ok"
        result.id = lesson.id
        if row is None:
            result.msg = "fail"
            
        return result