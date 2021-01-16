from django.db import models

# Create your models here.

class User_Test(models.Model):
    username = models.CharField(max_length=30,null=True)
    phone = models.CharField(max_length=10,null=True)
    password = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.username

