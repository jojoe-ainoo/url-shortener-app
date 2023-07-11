from django.core.management.base import BaseCommand
from books.models import Category, Country, Tag, Author, Book


class Command(BaseCommand):
    help = "Delete all instances of Book app from the database"

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Country.objects.all().delete()
        Tag.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All book related instances deleted."))
