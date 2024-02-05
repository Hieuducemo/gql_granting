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
test_reference_program_levels = createResolveReferenceTest(tableName='acprogramlevels', gqltype='AcProgramLevelTypeGQLModel', attributeNames=["id"])
test_query_program_levels_by_id = createByIdTest(tableName="acprogramlevels", queryEndpoint="programLevelById", attributeNames=["id"])

