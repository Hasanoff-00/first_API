from django.db import models
import string
import random
from django.contrib.auth.models import User

class URL(models.Model):
    original_url = models.URLField(max_length=200)
    short_code = models.CharField(max_length=6, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(4))
        if URL.objects.filter(short_code=short_code).exists():
            return self.generate_short_code()
        return short_code

    def __str__(self):
        return f'{self.original_url} -> {self.short_code}'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
