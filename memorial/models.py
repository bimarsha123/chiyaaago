from django.db import models
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Martyr(models.Model):
    class DateChoice(models.TextChoices):
        SEPT_8 = "sept_8", "September 8"
        SEPT_9 = "sept_9", "September 9"

    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=200)
    date = models.CharField(max_length=20, choices=DateChoice.choices, default=DateChoice.SEPT_8)
    description = models.TextField()
    image = models.ImageField(upload_to="martyrs/", null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_featured", "is_published"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("memorial:martyr_detail", kwargs={"slug": self.slug})


class TimelineEvent(models.Model):
    class DateChoice(models.TextChoices):
        SEPT_8 = "sept_8", "September 8"
        SEPT_9 = "sept_9", "September 9"

    date = models.CharField(max_length=20, choices=DateChoice.choices)
    time_of_day = models.CharField(max_length=50, help_text="e.g., Morning, Afternoon, Evening")
    event = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "order"]
        indexes = [models.Index(fields=["date", "order"])]

    def __str__(self):
        return f"{self.date} - {self.time_of_day}: {self.event[:50]}..."


class WitnessAccount(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, help_text="e.g., Protest Participant, Local Resident")
    testimonial = models.TextField()
    avatar_initials = models.CharField(max_length=4, blank=True)
    image = models.ImageField(upload_to="accounts/", null=True, blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return f"{self.name} - {self.role}"


class Pillar(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Lucide icon name (e.g., Megaphone, Shield)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.key


class ContactSubmission(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class NewsUpdate(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    image = models.ImageField(upload_to="news/", null=True, blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("memorial:news_detail", kwargs={"slug": self.slug})


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="gallery/")
    caption = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title or f"Gallery Image {self.pk}"
