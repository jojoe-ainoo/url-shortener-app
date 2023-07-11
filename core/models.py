import secrets
import os
from django.db import models

class Url(models.Model):
    url = models.URLField(max_length=255)
    hashed_url = models.CharField(max_length=10, blank=True)
    pin = models.CharField(max_length=6, default="", blank=True)

    def __str__(self):
        return f"{self.pk} - {self.url} - {self.hashed_url}"

    def save(self, *args, **kwargs):
        if not self.hashed_url:
            self.hashed_url = self.hash_url()
            self.pin = ""  # Set pin to an empty string if no custom hash is provided
        elif not self.pin:
            self.pin = self.generate_pin()  # Generate pin only when a custom hash is provided

        super().save(*args, **kwargs)


    def hash_url(self):
        token = secrets.token_urlsafe(16)[:10]
        return token

    def get_full_short_url(self):
        base_url = os.getenv("URL_SHORTENER_HOST", "http://localhost:8000")
        return f"{base_url}/{self.hashed_url}"

    def generate_pin(self):
        pin = secrets.randbelow(1000000)
        return f"{pin:06}"