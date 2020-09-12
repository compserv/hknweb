from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ..models import Rating, ICSR
from ..models.icsr import _chrono


@receiver(pre_delete, sender=Rating, dispatch_uid='rating_delete_signal')
def update_on_rating_delete(sender, instance, using, **kwargs):
    if _chrono(instance.rating_survey.survey_icsr.icsr_semester) == _chrono(instance.rating_question.recent_semester):
        all_ratings = Rating.recency_ordering(instance.rating_question.rating_set)
        if all_ratings.exists():
            newest_rating = all_ratings.first()
            instance.rating_question.current_text = newest_rating.question_text
            instance.rating_question.recent_semester = newest_rating.rating_survey.survey_icsr.icsr_semester
            instance.rating_question.save()
        else:
            instance.rating_question.current_text = None
            instance.rating_question.recent_semester = None
            instance.rating_question.save()


@receiver(pre_delete, sender=ICSR, dispatch_uid='icsr_delete_signal')
def update_on_icsr_delete(sender, instance, using, **kwargs):
    ##Instructors
    if _chrono(instance.icsr_semester) == _chrono(instance.icsr_instructor.recent_semester):
        all_icsrs = Rating.recency_ordering(instance.icsr_instructor.icsr_set)
        if all_icsrs.exists():
            newest_icsr = all_icsrs.first()
            instance.icsr_instructor.current_first_name = newest_icsr.first_name
            instance.icsr_instructor.current_last_name = newest_icsr.last_name
            instance.icsr_instructor.current_instructor_type = newest_icsr.instructor_type
            instance.icsr_instructor.recent_semester = newest_icsr.icsr_semester
            instance.icsr_instructor.save()
        else:
            instance.icsr_instructor.current_first_name = None
            instance.icsr_instructor.current_last_name = None
            instance.icsr_instructor.current_instructor_type = None
            instance.icsr_instructor.recent_semester = None
            instance.icsr_instructor.save()
        ##Courses
        all_icsrs = Rating.recency_ordering(instance.icsr_course.icsr_set)
        if all_icsrs.exists():
            newest_icsr = all_icsrs.first()
            instance.icsr_course.current_name = newest_icsr.course_name
            instance.icsr_course.current_number = newest_icsr.course_number
            instance.icsr_course.recent_semester = newest_icsr.icsr_semester
            instance.icsr_course.save()
        else:
            instance.icsr_course.current_name = None
            instance.icsr_course.current_number = None
            instance.icsr_course.recent_semester = None
            instance.icsr_course.save()
