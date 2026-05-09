from django.contrib import admin
from .models import (
    Martyr,
    TimelineEvent,
    WitnessAccount,
    Pillar,
    SiteSetting,
    ContactSubmission,
    NewsUpdate,
    GalleryImage,
    Category,
)


@admin.register(Martyr)
class MartyrAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "location", "date", "is_featured", "is_published", "created_at")
    list_filter = ("date", "is_featured", "is_published", "created_at")
    search_fields = ("name", "location", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_featured", "is_published")
    ordering = ("-created_at",)
    fieldsets = (
        ("Personal Information", {"fields": ("name", "age", "location", "date")}),
        ("Details", {"fields": ("description", "image")}),
        ("Status", {"fields": ("is_featured", "is_published", "slug")}),
    )


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("date", "time_of_day", "event", "order", "is_published")
    list_filter = ("date", "is_published")
    search_fields = ("event",)
    list_editable = ("order", "is_published")
    ordering = ("date", "order")


@admin.register(WitnessAccount)
class WitnessAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_featured", "is_published", "created_at")
    list_filter = ("is_featured", "is_published")
    search_fields = ("name", "role", "testimonial")
    list_editable = ("is_featured", "is_published")


@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "description")
    search_fields = ("key", "description")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("is_read",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"


@admin.register(NewsUpdate)
class NewsUpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "created_at")
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)
    ordering = ("-published_at", "-created_at")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "caption")
    list_editable = ("is_published", "order")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
