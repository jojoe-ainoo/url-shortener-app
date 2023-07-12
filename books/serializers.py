from rest_framework import serializers
from .models import Category, Country, Tag, Author, Book


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class AuthorSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Author
        fields = ["id", "name", "country"]

#  Book Serializer using new queryset method to modify meta calss
class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author__name")
    category_name = serializers.CharField(source="category__name")
    tags_names = serializers.ListField(source="tags__name")

    class Meta:
        # Use derived fileds [author_name, category_name, tag_names]
        # makes it faster to use derived  fields rather than serializing the entire models (unecessary serialization) 
        # could change based on project requirements
        model = Book
        fields = ["id", "title", "author_name", "category_name", "tags_names"]
