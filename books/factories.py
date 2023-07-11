import random

import factory
from factory.django import DjangoModelFactory
from .models import Category, Country, Tag, Author, Book


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Iterator(["Science Fiction", "Fantasy", "Mystery"])


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Faker("country")


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Iterator(["Adventure", "Romance", "Thriller"])


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker("name")
    country = factory.SubFactory(CountryFactory)


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence")
    author = factory.SubFactory(AuthorFactory)
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Use the extracted tags
            self.tags.set(extracted)
        else:
            # Create random tags
            num_tags = random.randint(1, 3)
            tags = TagFactory.create_batch(num_tags)
            self.tags.set(tags)
