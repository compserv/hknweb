# This script is to be copy-pasted into the db shell
# Change the value of the number of exported Instructorships

require "json"
require "set"


OUTPUT_FILE_NAME = "course_surveys_data.json"

instructorships = Instructorship.last(1000)

output = {
    "survey_answer" => [],
    "instructorship" => [],
    "klass" => Set[],
    "instructor" => Set[],
    "course" => Set[],
    "department" => Set[],
    "survey_question" => Set[],
}
post_process_model_types = {
    "klass" => Klass,
    "instructor" => Instructor,
    "course" => Course,
    "department" => Department,
    "survey_question" => SurveyQuestion,
}


instructorships.each do |iship|
    klass = Klass.find(iship.klass_id)
    instructor = Instructor.find(iship.instructor_id)
    course = Course.find(klass.course_id)
    dept = Department.find(course.department_id)

    output["instructorship"].append(iship)

    output["klass"].add(klass.id)
    output["instructor"].add(instructor.id)
    output["course"].add(course.id)
    output["department"].add(dept.id)

    survey_answers = SurveyAnswer.where(
        "instructorship_id = ?",
        iship.id,
    )
    survey_answers.each do |survey_answer|
        survey_question = SurveyQuestion.find(survey_answer.survey_question_id)

        output["survey_question"].add(survey_question.id)
        output["survey_answer"].append(survey_answer)
    end
end


post_process_model_types.each do |model_key, model_cls|
    output_models = []

    ids = output[model_key]
    ids.each do |id|
        model = model_cls.find(id)
        output_models.append(model)
    end

    output[model_key] = output_models
end


File.open(OUTPUT_FILE_NAME, "w") { |file| file.write(output.to_json) }
