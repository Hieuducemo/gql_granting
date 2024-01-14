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
test_reference_sujects = createResolveReferenceTest(tableName='acsubjects', gqltype='AcSubjectGQLModel', attributeNames=["id"])
test_query_subject_page = createPageTest(tableName="acsubjects", queryEndpoint="acsubjectPage")
test_query_subject_by_id = createByIdTest(tableName="acsubjects", queryEndpoint="acsubjectById")

test_subject_insert = createFrontendQuery(query="""
    mutation($programId: UUID!, $name: String!,$nameEn:String!) { 
        result: subjectInsert(subject: {programId: $programId, name: $name,nameEn: $nameEn}) { 
            id
            msg
            subject {
                id
                name
                program { id }
            }
        }
    }
    """, 
    variables={"programId": "2766fc9a-b095-11ed-9bd8-0242ac110002", "name": "new subject","nameEn": ""},
    asserts=[]
)

test_subject_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            subjectUpdate(subject: {id: $id,  lastchange: $lastchange}) {
                id
                msg
                subject {
                    id
                
                    lastchange
                }
            }
        }
    """,
    variables={"id": "ce250a68-b095-11ed-9bd8-0242ac110002", "lastchange":datetime.datetime},
    tableName="acsubjects"
)
