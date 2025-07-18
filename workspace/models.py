from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class StartupIdea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Stores user ID, not username. Works if user changes username.
    startup_name = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.TextField(default='General') # A single word that describes the startup idea, e.g. "technology", "food", "engineering", etc.

    def __str__(self):
        return self.startup_name

class StartupEvaluation(models.Model):
    startup = models.ForeignKey(StartupIdea, on_delete=models.CASCADE)
    evaluation_text = models.TextField()
    market_trends = models.TextField(default='')  # Optional field for market trends

    def __str__(self):
        return self.evaluation_text