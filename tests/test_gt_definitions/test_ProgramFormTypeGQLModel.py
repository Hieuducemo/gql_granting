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
test_reference_program_forms = createResolveReferenceTest(tableName='acprogramforms', gqltype='AcProgramFormTypeGQLModel', attributeNames=["id"])
test_query_program_forms_by_id = createByIdTest(tableName="acprogramforms", queryEndpoint="programFormById", attributeNames=["id"])

