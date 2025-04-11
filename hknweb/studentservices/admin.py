from django.contrib import admin

from hknweb.studentservices.models import (
    CourseGuideNode,
    CourseGuideAdjacencyList,
    CourseGuideGroup,
    CourseGuideParam,
    DepTour,
    Resume,
)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    fields = ["name", "email", "notes", "document", "uploaded_at", "critiques"]
    readonly_fields = ["uploaded_at", "email", "name", "document"]
    list_display = ("name", "notes", "document", "uploaded_at")
    list_filter = ("name", "notes", "document", "uploaded_at")


@admin.register(DepTour)
class ToursAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "confirmed",
        "datetime",
        "email",
        "phone",
        "comments",
        "deprel_comments",
    ]
    readonly_fields = ("name", "email", "phone", "comments")
    list_display = (
        "name",
        "confirmed",
        "email",
        "datetime",
        "date_submitted",
        "phone",
        "comments",
        "deprel_comments",
    )


@admin.register(CourseGuideNode)
class CourseGuideNodeAdmin(admin.ModelAdmin):
    fields = ["name", "is_title", "x_0", "y_0"]
    list_display = ["name", "is_title", "x_0", "y_0"]


@admin.register(CourseGuideAdjacencyList)
class CourseGuideAdjacencyListAdmin(admin.ModelAdmin):
    fields = ["source", "targets"]
    list_display = ["source"]
    filter_horizontal = ["targets"]


@admin.register(CourseGuideGroup)
class CourseGuideGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ["nodes"]


@admin.register(CourseGuideParam)
class CourseGuideParamAdmin(admin.ModelAdmin):
    fields = list_display = [
        "link_distance",
        "circle_radius",
        "force_strength",
        "marker_width",
        "marker_height",
    ]
