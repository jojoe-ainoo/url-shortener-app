from django.contrib import admin

# Register your models here.
# add admin site for category, country, tag, author, book

from .models import Category, Country, Tag, Author, Book

admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Book)
