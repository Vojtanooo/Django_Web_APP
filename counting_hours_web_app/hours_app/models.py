from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Day(models.Model):

    working_day = models.CharField(
        max_length=200, blank=False, primary_key=True)
    number_start = models.CharField(max_length=50, blank=False)
    number_end = models.CharField(max_length=50, blank=False)
    result = models.CharField(max_length=50, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("home")
