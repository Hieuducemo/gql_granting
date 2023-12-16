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

test_reference_semesters = createResolveReferenceTest(tableName='acsemesters', gqltype='SemesterGQLModel', attributeNames=["id", "order", "lastchange","credits", "subjects {id}","classification {id}"])
test_query_semester_page = createPageTest(tableName="acsemesters", queryEndpoint="acsemesterPage")

test_semester_insert = createFrontendQuery(query="""
    mutation($classificationtypeId: UUID!, $subjectId: UUID!) { 
        result: semesterInsert(semester: {classification: $id, subjectId: $id}) { 
            id
            msg
            semester {
                id
                
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new semester"},
    asserts=[]
)

test_semester_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            semesterUpdate(semester: {id: $id, lastchange: $lastchange}) {
                id
                msg
                semester {
                    id
                    lastchange
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "lastchange": datetime.datetime},
    tableName="acsemesters"
)
