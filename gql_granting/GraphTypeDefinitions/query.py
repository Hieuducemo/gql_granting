import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .AcLessonGQLModel import aclesson_by_id
    aclesson_by_id = aclesson_by_id 
    from .AcLessonGQLModel import aclesson_type_page
    aclesson_type_page = aclesson_type_page
    from .AcClassificationGQLModel import acclassification_page
    acclassification_page = acclassification_page
    from .AcClassificationGQLModel import acclassification_page_by_user
    acclassification_page_by_user = acclassification_page_by_user
    from .AcProgramGQLModel import program_by_id
    program_by_id = program_by_id
    from .AcProgramGQLModel import program_page 
    program_page = program_page 
    from .AcSemesterGQLModel import acsemester_page
    acsemester_page = acsemester_page 
    from .AcSubjectGQLModel import acsubject_by_id
    acsubject_by_id = acsubject_by_id 
    from .AcSubjectGQLModel import acsubject_page
    acsubject_page = acsubject_page
    from .AcTopicGQLModel import actopic_by_id 
    actopic_by_id = actopic_by_id
    pass
      