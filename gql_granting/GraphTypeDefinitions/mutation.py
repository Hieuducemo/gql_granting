import strawberry

@strawberry.type
class Mutation:
    from .AcClassificationGQLModel import classification_insert
    classification_insert = classification_insert
    from .AcProgramGQLModel import program_insert
    program_insert = program_insert 
    from .AcClassificationGQLModel import classification_update 
    classification_update= classification_update 
    from .AcProgramGQLModel import program_update
    program_update = program_update 
    from .AcTopicGQLModel import topic_insert 
    topic_insert = topic_insert
    from .AcTopicGQLModel import topic_update 
    topic_update = topic_update 
    from .AcSubjectGQLModel import subject_insert
    subject_insert = subject_insert 
    from .AcSubjectGQLModel import subject_update
    subject_update = subject_update 
    from .AcSemesterGQLModel import semester_insert
    semester_insert = semester_insert 
    from .AcSemesterGQLModel import semester_update 
    semester_update = semester_update 
    from .AcLessonGQLModel import lesson_insert
    lesson_insert= lesson_insert 
    from .AcLessonGQLModel import lesson_update 
    lesson_update = lesson_update 
    pass