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

test_reference_semesters = createResolveReferenceTest(tableName='acsemesters', gqltype='AcSemesterGQLModel', attributeNames=["id"])
test_query_semester_page = createPageTest(tableName="acsemesters", queryEndpoint="acsemesterPage")

test_semester_insert = createFrontendQuery(query="""
    mutation($classificationtypeId: UUID!, $subjectId: UUID!) { 
        result: semesterInsert(semester: {classificationtypeId: $classificationtypeId, subjectId: $subjectId}) { 
            id
            msg
            semester {
                classificationtype { id }
                subject { id }
            }
        }
    }
    """, 
    variables={"classificationtypeId": "a00a0642-b095-11ed-9bd8-0242ac110002", "subjectid": "ce250a68-b095-11ed-9bd8-0242ac110002"},
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
