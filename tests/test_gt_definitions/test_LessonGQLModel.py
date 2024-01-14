import pytest
from gql_granting.GraphTypeDefinitions import schema
import datetime
# from ..shared import (
#     prepare_demodata,
#     prepare_in_memory_sqllite,
#     get_demodata,
#     createContext,
# )
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_lessons = createResolveReferenceTest(tableName='aclessons', gqltype='AcLessonGQLModel', attributeNames=["id"])
test_query_lesson_by_id = createByIdTest(tableName="aclessons", queryEndpoint="aclessonById", attributeNames=["id"])

test_lesson_insert = createFrontendQuery(query="""
    mutation($topicId: UUID!, $typeId: UUID!) { 
        result: lessonInsert(lesson: {topicId: $topicId, typeId: $typeId}) { 
            id
            msg
            lesson {
                topic { id }
                type { id }
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new lesson", "topicId": "ce250b44-b095-11ed-9bd8-0242ac110002", "typeId": "e2b7cbf6-95e1-11ed-a1eb-0242ac120002"},
    asserts=[]
)

test_lesson_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            lessonUpdate(lesson: {id: $id, lastchange: $lastchange}) {
                id
                msg
                lesson {
                    id
                    lastchange
                }
            }
        }
    """,
    variables={"id": "ce250b8a-b095-11ed-9bd8-0242ac110002", "lastchange": datetime.datetime.now().isoformat()},
    tableName="aclessons"
)
