from typing import List, Union, Optional, Annotated
import strawberry 
import strawberry as strawberryA
#from .AcProgramGQLModel import AcProgramGQLModel
from contextlib import asynccontextmanager
from gql_granting.GraphResolvers import resolveProgramForGroup, resolveJSONForProgram
from .AcClassificationGQLModel import AcClassificationGQLModel
import uuid
AcProgramGQLModel= Annotated["AcProgramGQLModel",strawberryA.lazy(".AcProgramGQLModel")]
@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

def getLoaders(info):
    return info.context['all']

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
    return cls(id=id)

@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: uuid.UUID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return GroupGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz
    async def program(
        self, info: strawberryA.types.Info
    ) -> Union["AcProgramGQLModel", None]:
        async with withInfo(info) as session:
            result = await resolveProgramForGroup(session, id)
            return result


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: uuid.UUID = strawberryA.federation.field(external=True)
    @classmethod
    async def resolve_reference(cls, id:uuid.UUID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,self.id)
#         return result


    @strawberryA.field(description="""List of programs which the user is studying""")
    async def study_programs(self, info: strawberryA.types.Info) -> List['AcProgramGQLModel']:
         
        loader = getLoaders(info).programstudents
        result = await loader.filter_by(student_id=self.id)       
        return result
    
    @strawberryA.field(description="""List of programs which the user is studying""")
    async def classifications(self, info: strawberryA.types.Info) -> List['AcClassificationGQLModel']:
        loader = getLoaders(info).classifications
        result = await loader.filter_by(user_id=self.id)       
        return result
 
from gql_granting.Dataloaders import getLoadersFromInfo 
    
@strawberry.federation.type(extend=True, keys=["id"])
class RBACObjectGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @classmethod
    async def resolve_roles(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).authorizations
        authorizedroles = await loader.load(id)
        return authorizedroles