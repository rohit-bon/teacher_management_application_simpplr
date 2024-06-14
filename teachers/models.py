from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=250)
    age = models.IntegerField()
    date_of_birth = models.DateField()
    classes_number = models.IntegerField()
    
    def __str__(self):
        return self.full_name