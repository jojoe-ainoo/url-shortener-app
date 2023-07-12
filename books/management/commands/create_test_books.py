from django.core.management.base import BaseCommand
from books.factories import BookFactory
import time

class Command(BaseCommand):
    help = "Create test books for endpoint performance testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, nargs="?", default=100, help="Number of books to create"
        )

    def handle(self, *args, **options):
        count = options["count"]
        start_time = time.time()
    
        BookFactory.create_batch(count)
        execution_time = time.time() - start_time

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} test books in {execution_time:.2f} seconds.")
        )
