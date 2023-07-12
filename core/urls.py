from django.urls import path

from .views import HomeView,  RetrieveView, EditView, URLListView, RedirectView


urlpatterns =[
    path("", HomeView.as_view(), name="home_page"),
    path("retrieve/", RetrieveView.as_view(), name="retrieve_url"),
    path("urls/", URLListView.as_view(), name="url_list"),
    path("edit/<str:hashed_url>/", EditView.as_view(), name="edit_url"),
    path("<str:hashed_url>/", RedirectView.as_view(), name="redirect_url"),
]