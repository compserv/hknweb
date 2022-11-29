from django.test import TestCase

from django.urls import reverse

from hknweb.studentservices.models import (
    CourseGuideParam,
    CourseGuideGroup,
    CourseGuideNode,
    CourseGuideAdjacencyList,
)


class CourseGuideViewTests(TestCase):
    def test_course_guide_get(self):
        CourseGuideParam.objects.create(
            link_distance=5,
            circle_radius=5,
            force_strength=5,
            marker_width=5,
            marker_height=5,
        )
        response = self.client.get(reverse("studentservices:course_guide"))

        self.assertEqual(response.status_code, 200)

    def test_course_guide_data_get(self):
        node1 = CourseGuideNode.objects.create(name="test_node_name_1")
        node2 = CourseGuideNode.objects.create(name="test_node_name_2")
        node3 = CourseGuideNode.objects.create(name="test_node_name_3")
        node4 = CourseGuideNode.objects.create(name="test_node_name_4")

        group = CourseGuideGroup.objects.create(name="test_group_name_1")
        group.nodes.add(node1)
        group.nodes.add(node3)
        group.save()
        group = CourseGuideGroup.objects.create(name="test_group_name_2")
        group.nodes.add(node2)
        group.save()

        al = CourseGuideAdjacencyList.objects.create(source=node1)
        al.targets.add(node2)
        al.targets.add(node3)
        al.save()
        al = CourseGuideAdjacencyList.objects.create(source=node4)

        response = self.client.get(
            reverse("studentservices:course_guide_data")
            + "?groups=bob,test_group_name_1"
        )

        self.assertEqual(response.status_code, 200)
