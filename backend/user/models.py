from django.db import models

class User(models.Model):
    name  = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
 
    def __str__(self):
        return self.name