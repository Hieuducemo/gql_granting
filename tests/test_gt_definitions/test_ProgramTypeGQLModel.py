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

test_reference_programs = createResolveReferenceTest(tableName='acprogramtypes', gqltype='AcProgramTypeGQLModel', attributeNames=["id"])
test_query_program_type_by_id = createByIdTest(tableName="acprogramtypes", queryEndpoint="programTypeById")


test_program_type_insert = createFrontendQuery(query="""
    mutation($formId: UUID!, $name: String!,$languageId: UUID!,$levelId:UUID!,$nameEn:String!,$titleId:UUID!) { 
        result: programTypeInsert(programType: {formId: $formId, name: $name,languageId: $languageId,levelId:$levelId,nameEn:$nameEn,titleId:$titleId}) { 
            id
            msg
            programType {
                id
                name
                nameEn
                
                
            }
        }
    }
    """, 
    variables={"formId": "19018d2c-930e-11ed-9b95-0242ac110002", "name": "new program type","languageId":"36e9a40a-930e-11ed-9b95-0242ac110002","levelId":"5c549cae-930e-11ed-9b95-0242ac110002","nameEn":"dasdddddda","titleId":"d1431d9c-930e-11ed-9b95-0242ac110002"},
    asserts=[]
)

test_program_type_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $lastchange: DateTime!) {
            programTypeUpdate(programType: {id: $id, lastchange: $lastchange}) {
                id
                msg
                programType {
                    id
                    lastchange
                }
            }
        }
    """,
    variables={"id": "fd4f0980-9315-11ed-9b95-0242ac110002", "lastchange": datetime.datetime.now().isoformat()},
    tableName="acprogramtypes"
)
