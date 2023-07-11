from django.core.management.base import BaseCommand
from books.factories import BookFactory


class Command(BaseCommand):
    help = "Create test books for endpoint performance testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, nargs="?", default=100, help="Number of books to create"
        )

    def handle(self, *args, **options):
        count = options["count"]
        BookFactory.create_batch(count)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} test books.")
        )
