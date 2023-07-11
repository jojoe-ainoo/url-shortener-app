from django.urls import path

from .views import HomeView,  RetrieveView, EditView, URLListView, RedirectView


# urlpatterns = [
#     path("", HomeView.as_view(), name="home_page"),
#     # path("<str:hashed_url>/", RedirectView.as_view(), name="redirect_to_original_url"),
#     path("<str:hashed_url>/", UrlDetailView.as_view(), name="url_detail"),
#     path("<str:hashed_url>/edit/", UrlDetailView.edit_url, name="edit_url"),
# ]

# urlpatterns = [
#     path("", HomeView.as_view(), name="home_page"),
#     path("<str:hashed_url>/", RedirectView.as_view(), name="redirect_to_original_url"),
#     path("<str:hashed_url>/detail/", UrlDetailView.as_view(), name="url_detail"),
#     path("<str:hashed_url>/edit/", UrlEditView.as_view(), name="edit_original_url"),
# ]

# urlpatterns = [
#     path("", HomeView.as_view(), name="home_page"),
#     path("retrieve/", RetrieveView.as_view(), name="retrieve_url"),
#     path("edit/<str:hashed_url>/", EditView.as_view(), name="edit_url"),
#     path("urls/", URLListView.as_view(), name="url_list"),
# ]

urlpatterns =[
    path("", HomeView.as_view(), name="home_page"),
    path("retrieve/", RetrieveView.as_view(), name="retrieve_url"),
    path("urls/", URLListView.as_view(), name="url_list"),
    path("edit/<str:hashed_url>/", EditView.as_view(), name="edit_url"),
    path("<str:hashed_url>/", RedirectView.as_view(), name="redirect_url"),
]