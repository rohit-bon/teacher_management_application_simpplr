from django.db import models
from django.forms import ValidationError


class Teacher(models.Model):
    full_name = models.CharField(max_length=250)
    age = models.IntegerField()
    date_of_birth = models.DateField()
    number_of_classes = models.IntegerField()
    
    class Meta:
        unique_together = ('full_name', 'date_of_birth')
    
    def __str__(self):
        return self.full_name