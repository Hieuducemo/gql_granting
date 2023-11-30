import strawberry
import datetime
import asyncio
import strawberry as strawberryA

#from .AcSemesterGQLModel import AcSemesterGQLModel
#from .AcLessonGQLModel import AcLessonGQLModel

from typing import Optional, List, Union, Annotated
def getLoaders(info):
    return info.context['all']
def getUser(info):
    return info.context["user"]

AcSemesterGQLModel= Annotated["AcSemesterGQLModel",strawberryA.lazy(".AcSemesterGQLModel")]
AcLessonGQLModel= Annotated["AcLessonGQLModel",strawberryA.lazy(".AcLessonGQLModel")]

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which represents a theme included in semester of subject""",
)
class AcTopicGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).topics
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name ("Introduction")""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""english name ("Introduction")""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""datetime lastchange""")
    def lastchange(self) -> str:
        return self.lastchange

    @strawberryA.field(description="""order (1)""")
    def order(self) -> Union[int, None]:
        return self.order

    @strawberryA.field(description="""Semester of subject which owns the topic""")
    async def semester(self, info: strawberryA.types.Info) -> Optional["AcSemesterGQLModel"]:
        from .AcSemesterGQLModel import AcSemesterGQLModel  
        result = await AcSemesterGQLModel.resolve_reference(info, self.semester_id)
        return result

    @strawberryA.field(description="""Lessons for a topic""")
    async def lessons(self, info: strawberryA.types.Info) -> List["AcLessonGQLModel"]:
        loader = getLoaders(info).lessons
        result = await loader.filter_by(topic_id=self.id)
        return result

#################################################
#
# Special fields for query
#
#################################################
from uuid import UUID 
@strawberryA.field(description="""Finds a topic by its id""")
async def actopic_by_id(
        self, info: strawberryA.types.Info, id: UUID
    ) -> Union["AcTopicGQLModel", None]:
        result = await AcTopicGQLModel.resolve_reference(info, id)
        return result


#################################################
#
# Special fields for mutation
#
#################################################

@strawberryA.input
class TopicInsertGQLModel:
    semester_id: strawberryA.ID
    order: Optional[int] = 0
    name: Optional[str] = "New Topic"
    name_en: Optional[str] = "New Topic"
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class TopicUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    order: Optional[int] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberryA.type
class TopicResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of topic operation""")
    async def topic(self, info: strawberryA.types.Info) -> Union[AcTopicGQLModel, None]:
        result = await AcTopicGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.mutation(description="""Adds new study topic""")
async def topic_insert(self, info: strawberryA.types.Info, topic: TopicInsertGQLModel) -> TopicResultGQLModel:
        loader = getLoaders(info).topics
        row = await loader.insert(topic)
        result = TopicResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

@strawberryA.mutation(description="""Update the study topic""")
async def topic_update(self, info: strawberryA.types.Info, topic: TopicUpdateGQLModel) -> TopicResultGQLModel:
        loader = getLoaders(info).topics
        row = await loader.update(topic)
        result = TopicResultGQLModel()
        result.msg = "ok"
        result.id = topic.id
        if row is None:
            result.msg = "fail"
            
        return result