import unittest
import pdb

pdb.set_trace()
from hknweb.academics.models.base_models import AcademicEntity
from hknweb.academics.models.icsr import ICSR
from hknweb.academics.models.logistics import Instructor, Course, Department, Semester


class DBTestCase(unittest.TestCase):
    def setUp(self):
        c = Course.objects.create()
        d = Department.objects.create(name="Electrical Engineering and Computer Science", abbr="EECS")
        s = Semester.objects.create(year=2020, year_section="Fa")
        for i in range(20):
            i = Instructor.objects.create(instructor_id=str(i))
            ICSR.objects.create(icsr_instructor=i, icsr_course=c, icsr_semester=s, icsr_department=d,
                                first_name="Anant {}".format(i),
                                last_name="Sahai {}".format(i), course_number="100", course_name="CS61A",
                                section_type="",
                                section_number="", instructor_type="Alien")

    def test_merge(self):
        AcademicEntity.merge(Instructor.objects.get("1"), [Instructor.objects.get(str(i)) for i in range(2, 5)])
        self.assertEqual(Instructor.objects.all().count(), 17)
        self.assertEqual(ICSR.objects.get(first_name="Anant 3").icsr_instructor.id,
                         Instructor.objects.get("1").id)


if __name__ == '__main__':
    unittest.main()
