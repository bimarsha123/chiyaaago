from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    FormView,
)
from django.db.models import Q, Count
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Martyr,
    TimelineEvent,
    WitnessAccount,
    Pillar,
    ContactSubmission,
    NewsUpdate,
    GalleryImage,
)
from .forms import ContactForm


class HomeView(TemplateView):
    template_name = "memorial/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_martyrs"] = Martyr.objects.filter(is_published=True, is_featured=True)[:4]
        context["featured_accounts"] = WitnessAccount.objects.filter(is_published=True, is_featured=True)[:3]
        context["pillars"] = Pillar.objects.filter(is_active=True)
        context["sept8_events"] = TimelineEvent.objects.filter(
            date=TimelineEvent.DateChoice.SEPT_8, is_published=True
        ).order_by("order")
        context["sept9_events"] = TimelineEvent.objects.filter(
            date=TimelineEvent.DateChoice.SEPT_9, is_published=True
        ).order_by("order")
        context["total_martyrs"] = Martyr.objects.filter(is_published=True).count()
        context["recent_news"] = NewsUpdate.objects.filter(is_published=True)[:3]
        context["gallery_images"] = GalleryImage.objects.filter(is_published=True)[:6]
        return context


class AboutView(TemplateView):
    template_name = "memorial/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_martyrs"] = Martyr.objects.filter(is_published=True).count()
        context["recent_news"] = NewsUpdate.objects.filter(is_published=True)[:3]
        return context


class MartyrListView(ListView):
    model = Martyr
    template_name = "memorial/martyrs_list.html"
    context_object_name = "martyrs"
    paginate_by = settings.MARTYRS_PER_PAGE

    def get_queryset(self):
        queryset = Martyr.objects.filter(is_published=True)
        date_filter = self.request.GET.get("date")
        search_query = self.request.GET.get("q")

        if date_filter:
            queryset = queryset.filter(date=date_filter)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(location__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date_filter"] = self.request.GET.get("date", "")
        context["search_query"] = self.request.GET.get("q", "")
        context["total_count"] = Martyr.objects.filter(is_published=True).count()
        return context


class MartyrDetailView(DetailView):
    model = Martyr
    template_name = "memorial/martyr_detail.html"
    context_object_name = "martyr"

    def get_queryset(self):
        return Martyr.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_martyrs"] = Martyr.objects.filter(
            is_published=True, date=self.object.date
        ).exclude(pk=self.object.pk)[:3]
        return context


class TimelineView(TemplateView):
    template_name = "memorial/timeline.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sept8_events"] = TimelineEvent.objects.filter(
            date=TimelineEvent.DateChoice.SEPT_8, is_published=True
        ).order_by("order")
        context["sept9_events"] = TimelineEvent.objects.filter(
            date=TimelineEvent.DateChoice.SEPT_9, is_published=True
        ).order_by("order")
        return context


class VoicesView(ListView):
    model = WitnessAccount
    template_name = "memorial/voices.html"
    context_object_name = "accounts"
    paginate_by = settings.ACCOUNTS_PER_PAGE

    def get_queryset(self):
        return WitnessAccount.objects.filter(is_published=True)


class RemembranceView(TemplateView):
    template_name = "memorial/remembrance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pillars"] = Pillar.objects.filter(is_active=True)
        return context


class ContactView(FormView):
    template_name = "memorial/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("memorial:contact_success")

    def form_valid(self, form):
        submission = ContactSubmission.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            subject=form.cleaned_data["subject"],
            message=form.cleaned_data["message"],
        )

        # Send email notification
        if settings.EMAIL_HOST_USER:
            try:
                send_mail(
                    subject=f"Memorial Contact: {form.cleaned_data['subject']}",
                    message=form.cleaned_data["message"],
                    from_email=form.cleaned_data["email"],
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
            except Exception:
                pass

        messages.success(self.request, "Your message has been sent. Thank you for reaching out.")
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = "memorial/contact_success.html"


class SearchView(ListView):
    template_name = "memorial/search_results.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return Martyr.objects.none()

        martyrs = Martyr.objects.filter(
            Q(name__icontains=query)
            | Q(location__icontains=query)
            | Q(description__icontains=query),
            is_published=True,
        )

        accounts = WitnessAccount.objects.filter(
            Q(name__icontains=query)
            | Q(role__icontains=query)
            | Q(testimonial__icontains=query),
            is_published=True,
        )

        news = NewsUpdate.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True,
        )

        return martyrs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()

        context["query"] = query
        context["martyrs_count"] = Martyr.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query), is_published=True
        ).count()
        context["accounts_count"] = WitnessAccount.objects.filter(
            Q(name__icontains=query) | Q(testimonial__icontains=query), is_published=True
        ).count()
        context["news_count"] = NewsUpdate.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query), is_published=True
        ).count()
        return context


class NewsListView(ListView):
    model = NewsUpdate
    template_name = "memorial/news_list.html"
    context_object_name = "news"
    paginate_by = 10

    def get_queryset(self):
        return NewsUpdate.objects.filter(is_published=True)


class NewsDetailView(DetailView):
    model = NewsUpdate
    template_name = "memorial/news_detail.html"
    context_object_name = "news_item"

    def get_queryset(self):
        return NewsUpdate.objects.filter(is_published=True)


class GalleryView(ListView):
    model = GalleryImage
    template_name = "memorial/gallery.html"
    context_object_name = "images"
    paginate_by = 12

    def get_queryset(self):
        return GalleryImage.objects.filter(is_published=True).order_by("order", "-created_at")
