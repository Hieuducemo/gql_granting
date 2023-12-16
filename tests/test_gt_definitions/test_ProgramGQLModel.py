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

test_reference_forms = createResolveReferenceTest(tableName='acprograms', gqltype='ProgramGQLModel', attributeNames=["id", "name", "lastchange", "subjects {id}","student {id}"])
test_query_form_by_id = createByIdTest(tableName="acprograms", queryEndpoint="programById")
test_query_form_page = createPageTest(tableName="acprograms", queryEndpoint="programPage")

test_program_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!) { 
        result: formInsert(form: {id: $id, name: $name}) { 
            id
            msg
            form {
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
            formUpdate(form: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                form {
                    id
                    name
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="acprograms"
)
