from django.db import models

# Create your models here.
class Headline(models.Model):
    headline = models.CharField(max_length=500)
    newspaper = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=1000)
    day_order = models.PositiveIntegerField()

    def __str__(self):
        return self.headline


