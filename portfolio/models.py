from django.db import models

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_picture = models.ImageField()
    urli = models.CharField(max_length=200)


    def __str__(self):
        return self.title