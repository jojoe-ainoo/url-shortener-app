from django.urls import path

from .views import HomeView, RedirectView


urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("<str:hashed_url>/", RedirectView.as_view(), name="redirect_to_original_url"),
]

