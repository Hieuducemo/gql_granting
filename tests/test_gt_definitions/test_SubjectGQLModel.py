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

test_reference_sujects = createResolveReferenceTest(tableName='acsubjects', gqltype='AcSubjectGQLModel', attributeNames=["id", "name", "lastchange", "program {id}","semesters {id}"])
test_query_subject_page = createPageTest(tableName="acsubjects", queryEndpoint="acsubjectPage")
test_query_subject_by_id = createByIdTest(tableName="acsubjects", queryEndpoint="acsubjectById")

test_program_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!,$nameEn:String!) { 
        result: subjectInsert(subject: {id: $id, name: $name,nameEn: $nameEn}) { 
            id
            msg
            subject {
                id
                name
               
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new subject"},
    asserts=[]
)

test_program_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            programUpdate(program: {id: $id,  lastchange: $lastchange}) {
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
    tableName="acsubjects"
)
