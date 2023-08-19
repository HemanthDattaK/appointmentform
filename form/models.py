from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phonenumber= models.IntegerField() 
    place = models.CharField(max_length=100) 
    purpose = models.CharField(max_length=100)
   
