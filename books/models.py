from django.db import models
from users.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='covers', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publish = models.BooleanField()
    
    def __str__(self):
        return self.title