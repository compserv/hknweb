from django.contrib import admin

from hknweb.studentservices.models import (
    CourseGuideNode,
    CourseGuideAdjacencyList,
    CourseGuideGroup,
    DepTour,
    Resume,
    ReviewSession,
)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    fields = ["name", "email", "notes", "document", "uploaded_at", "critiques"]
    readonly_fields = ["uploaded_at", "email", "name", "document"]
    list_display = ("name", "notes", "document", "uploaded_at")
    list_filter = ("name", "notes", "document", "uploaded_at")


@admin.register(ReviewSession)
class ReviewSessionAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "slug",
        "start_time",
        "end_time",
        "location",
        "description",
        "created_by",
        "created_at",
    ]
    # NOTE: created_by should be read only, but I don't know how to set it to default to current user
    readonly_fields = ["created_at"]
    list_display = ("name", "start_time", "location", "created_by", "created_at")
    list_filter = ["start_time", "created_at", "location", "created_by"]
    search_fields = [
        "name",
        "created_by__username",
        "created_by__first_name",
        "created_by__last_name",
    ]
    ordering = ["-created_at"]
    autocomplete_fields = ["created_by"]


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
