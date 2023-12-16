import pytest
from gql_granting.GraphTypeDefinitions import schema
import datetime
from ..shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)
from ..gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_lessons = createResolveReferenceTest(tableName='aclessons', gqltype='ProgramGQLModel', attributeNames=["id", "name", "lastchange", "topic {id}"])
test_query_lesson_by_id = createByIdTest(tableName="aclessons", queryEndpoint="aclessonById")

test_lesson_insert = createFrontendQuery(query="""
    mutation($topicId: UUID!, $typeId: UUID!) { 
        result: lessonInsert(lesson: {topicId: $topicId, typeId: $typeId}) { 
            topicId
            msg
            lesson {
                topicId
                typeId
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new lesson"},
    asserts=[]
)

test_lesson_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            lessonUpdate(lesson: {id: $id, lastchange: $lastchange}) {
                id
                msg
                program {
                    id
                    lastchange
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "lastchange":datetime.datetime},
    tableName="aclessons"
)
