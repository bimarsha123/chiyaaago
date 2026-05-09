from django.urls import path
from . import views

app_name = "memorial"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("martyrs/", views.MartyrListView.as_view(), name="martyrs_list"),
    path("martyrs/<slug:slug>/", views.MartyrDetailView.as_view(), name="martyr_detail"),
    path("timeline/", views.TimelineView.as_view(), name="timeline"),
    path("voices/", views.VoicesView.as_view(), name="voices"),
    path("remembrance/", views.RemembranceView.as_view(), name="remembrance"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("contact/success/", views.ContactSuccessView.as_view(), name="contact_success"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("gallery/", views.GalleryView.as_view(), name="gallery"),
]
