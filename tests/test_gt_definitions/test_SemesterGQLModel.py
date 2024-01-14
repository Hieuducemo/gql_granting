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

test_reference_semesters = createResolveReferenceTest(tableName='acsemesters', gqltype='AcSemesterGQLModel', attributeNames=["id"])
test_query_semester_page = createPageTest(tableName="acsemesters", queryEndpoint="acsemesterPage")

test_semester_insert = createFrontendQuery(query="""
    mutation($classificationtypeId: UUID!, $subjectId: UUID!) { 
        result: semesterInsert(semester: {classificationtypeId: $classificationtypeId, subjectId: $subjectId}) { 
            id
            msg
            semester {
                classificationType { id }
                subject { id }
            }
        }
    }
    """, 
    variables={"classificationtypeId": "a00a0642-b095-11ed-9bd8-0242ac110002", "subjectId": "3ed497ea-ab40-4e94-a93e-9d9627497652"},
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
    variables={"id": "85c0db4a-148c-477e-ad5b-3985eaba1f90", "lastchange": datetime.datetime.now().isoformat()},
    tableName="acsemesters"
)
