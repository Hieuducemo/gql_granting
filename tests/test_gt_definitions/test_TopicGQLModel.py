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

test_reference_topics = createResolveReferenceTest(tableName='actopics', gqltype='AcTopicGQLModel', attributeNames=["id", "name","order", "lastchange", "semester {id}","lessons {id}"])
test_query_topic_by_id = createByIdTest(tableName="actopics", queryEndpoint="actopicById")


test_topic_insert = createFrontendQuery(query="""
    mutation($semesterId: UUID!) { 
        result: topicInsert(semester: {semesterId: $id}) { 
            id
            msg
            topic {
                id
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3"},
    asserts=[]
)

test_topic_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            topicUpdate(semester: {id: $id, lastchange: $lastchange}) {
                id
                msg
                topic {
                    id
                    lastchange 
                    name
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002","name":"new name", "lastchange": datetime.datetime},
    tableName="actopics"
)
