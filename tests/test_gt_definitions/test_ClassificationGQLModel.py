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

test_reference_classifications = createResolveReferenceTest(tableName='acclassifications', gqltype='AcClassificationGQLModel', attributeNames=["id"])
test_query_classification_page = createPageTest(tableName="acclassifications", queryEndpoint="acclassificationPage", attributeNames=["id"])

test_classification_insert = createFrontendQuery(query="""
    mutation($order: Int!, $semesterId: UUID!, $userId: UUID!, $classificationlevelId: UUID!,$classificationtypeId: UUID!) { 
        result: classificationInsert(classification: {order: $order, semesterId: $semesterId, userId: $userId, classificationlevelId: $classificationlevelId, classificationtypeId: $classificationtypeId}) { 
            id 
            msg
            classification {
                order
                user { id }
                semester { id }
               
            }
        }
    }
    """, 
    variables={"semesterId": "ce250af4-b095-11ed-9bd8-0242ac110002", "order": 2, "userId":"2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "classificationlevelId": "5fae9dd8-b095-11ed-9bd8-0242ac110002","classificationtypeId":"a00a0642-b095-11ed-9bd8-0242ac110002"},
    asserts=[]
)

test_classification_update = createUpdateQuery(
    query="""
        mutation($classificationlevelId: UUID!, $id: UUID!, $lastchange: DateTime!) {
            classificationUpdate(classification: {classificationlevelId: $classificationlevelId,id: $id, lastchange: $lastchange}) {
                id
                msg
                classification{
                    id
                   
                    lastchange
                }
            } 
        }
    """,
    variables={"id": "ce250bd0-b095-11ed-9bd8-0242ac110002", "classificationlevelId": "5fae9dd8-b095-11ed-9bd8-0242ac110002","lastchange": datetime.datetime.now().isoformat()},
    tableName="acclassifications"
)
