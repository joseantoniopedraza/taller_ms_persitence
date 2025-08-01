from django.db import models

# Create your models here.

class Tenders(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.code} - {self.title}"
