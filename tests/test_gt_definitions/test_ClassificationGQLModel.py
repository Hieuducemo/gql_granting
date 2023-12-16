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

test_reference_classifications = createResolveReferenceTest(tableName='acclassifications', gqltype='ClassificationGQLModel', attributeNames=["id", "lastchange","date", "user {id}","semesters {id}"])
test_query_classification_page = createPageTest(tableName="acclassifications", queryEndpoint="acclassificationPage")

test_classification_insert = createFrontendQuery(query="""
    mutation($order: int!, $semesterId: UUID!,$userId:UUID!) { 
        result: classificationInsert(classification: {order: $order, semesterId: $semesterId,userId: $userId}) { 
            semesterId
            msg
            classification {
                order
                userId
               
            }
        }
    }
    """, 
    variables={"semesterId": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "order":"2","userId":"ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3"},
    asserts=[]
)

test_program_update = createUpdateQuery(
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
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "lastchange":datetime.datetime,"classificationlevelId":"190d578c-afb1-11ed-9bd8-0242ac110002"},
    tableName="acclassifications"
)
