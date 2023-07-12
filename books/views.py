from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


# class BookListAPIView(generics.ListAPIView):
#     # select_related - use a join query for fetch for related fields author and category
#     # prefetch_related - retireve related objects separate from main query and cache them to minimize database hits
#     queryset = Book.objects.select_related("author", "category").prefetch_related("tags")
#     serializer_class = BookSerializer


class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    # overide query set method
    def get_queryset(self):
        # select_related - use a join query for fetch for related fields author and category
        # prefetch_related - retireve related objects separate from main query and cache them to minimize database hits
        # only & values to fecth only necessary fields
        return Book.objects.only("id", "title").select_related("author", "category").prefetch_related("tags").values("id", "title", "author__name", "category__name", "tags__name")
