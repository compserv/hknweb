from django.test import TestCase

from hknweb.studentservices.models import (
    CourseGuideParam,
    CourseGuideGroup,
    CourseGuideNode,
    CourseGuideAdjacencyList,
)


class CourseGuideModelTests(TestCase):
    def test_course_guide_models(self):
        param = CourseGuideParam.objects.create(
            link_distance=5,
            circle_radius=5,
            force_strength=5,
            marker_width=5,
            marker_height=5,
        )
        node = CourseGuideNode.objects.create(name="test_node_name_1")
        group = CourseGuideGroup.objects.create(name="test_group_name_1")
        al = CourseGuideAdjacencyList.objects.create(source=node)

        to_repr = [param, node, group, al]
        for r in to_repr:
            self.assertTrue(repr(r))
