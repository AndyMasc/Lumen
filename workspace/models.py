from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class startupIdea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Stores user ID, not username. Works if user changes username.
    startupName = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.startupName