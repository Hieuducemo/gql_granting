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

test_query_classification_type_by_id = createByIdTest(tableName="acclassifications", queryEndpoint="classificationTypeById",attributeNames=["id"])
test_query_classification_type_page = createPageTest(tableName="acclassificationtypes", queryEndpoint="acclassificationTypePage")