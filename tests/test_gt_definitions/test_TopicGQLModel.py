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

test_reference_topics = createResolveReferenceTest(tableName='actopics', gqltype='AcTopicGQLModel', attributeNames=["id"])
test_query_topic_by_id = createByIdTest(tableName="actopics", queryEndpoint="actopicById")


test_topic_insert = createFrontendQuery(query="""
    mutation($semesterId: UUID!) { 
        result: topicInsert(topic: {semesterId: $semesterId}) {   
            msg
            topic {
                semester { id }
            }
        }
    }
    """, 
    variables={"semesterId": "ce250af4-b095-11ed-9bd8-0242ac110002"},
    asserts=[]
)

test_topic_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            topicUpdate(topic: {id: $id, lastchange: $lastchange}) {
                id
                msg
                topic {
                    id
                    lastchange 
                }
            }
        }
    """,
    variables={"id": "ce250b44-b095-11ed-9bd8-0242ac110002", "lastchange": datetime.datetime},
    tableName="actopics"
)
