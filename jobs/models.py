from django.db import models

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    company = models.CharField(max_length=255, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    experience = models.CharField(max_length=255)
    application_link = models.URLField()

    def __str__(self):
        return self.title
