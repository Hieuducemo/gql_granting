# import strawberry
# import datetime
# import asyncio
# import strawberry as strawberryA
# import uuid
# from typing import Optional, List, Union, Annotated

# def getLoaders(info):
#     return info.context['all']
# def getUser(info):
#     return info.context["user"]

# #UserGQLModel= Annotated["UserGQLModel",strawberryA.lazy(".granting")]

# @strawberryA.federation.type(keys=["id"], description="Study program editor")
# class AcProgramEditorGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: uuid.UUID):
#         loader = getLoaders(info).programs
#         result = await loader.load(id)
#         if result is not None:
#             result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
#         return result

#     @strawberryA.field(description="primary key")
#     def id(self) -> uuid.UUID:
#         return self.id

#     # change name, add subject, delete subject

#     # @strawberryA.field(description="groups linked the program")
#     # async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]:
#     #     async with withInfo(info) as session:
#     #         links = await resolveGroupIdsForProgram(session, self.id)
#     #         result = list(map(lambda item: GroupGQLModel(id=item), links))
#     #         return result


