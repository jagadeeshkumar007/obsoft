from django.db import models

# Create your models here.
class Userform(models.Model):
    username= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    Designation= models.CharField(max_length=100)
    DateofJoinning= models.DateField()
    Biometricid= models.CharField(max_length=100,primary_key=True)
    password= models.CharField(max_length=100)
    