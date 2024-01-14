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

test_reference_programs = createResolveReferenceTest(tableName='acprograms', gqltype='AcProgramGQLModel', attributeNames=["id"])
test_query_program_by_id = createByIdTest(tableName="acprograms", queryEndpoint="programById")
test_query_program_page = createPageTest(tableName="acprograms", queryEndpoint="programPage")

test_program_insert = createFrontendQuery(query="""
    mutation($typeId: UUID!, $name: String!) { 
        result: programInsert(program: {typeId: $typeId, name: $name}) { 
            id
            msg
            program {
                id
                name
                type { id }
            }
        }
    }
    """, 
    variables={"typeId": "fd4f0980-9315-11ed-9b95-0242ac110002", "name": "new program"},
    asserts=[]
)

test_program_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            programUpdate(program: {id: $id, lastchange: $lastchange}) {
                id
                msg
                program {
                    id
                    
                }
            }
        }
    """,
    variables={"id": "2766fc9a-b095-11ed-9bd8-0242ac110002", "lastchange": datetime.datetime.now().isoformat()},
    tableName="acprograms"
)
