import pytest
from gql_granting.GraphTypeDefinitions import schema

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

test_reference_programs = createResolveReferenceTest(tableName='acprograms', gqltype='ProgramGQLModel', attributeNames=["id", "name"])
test_query_program_by_id = createByIdTest(tableName="acprograms", queryEndpoint="programById")
test_query_program_page = createPageTest(tableName="acprograms", queryEndpoint="programPage")

test_program_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!) { 
        result: programInsert(program: {id: $id, name: $name}) { 
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
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new program"},
    asserts=[]
)

test_program_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            programUpdate(program: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                program {
                    id
                    name
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="acprograms"
)
