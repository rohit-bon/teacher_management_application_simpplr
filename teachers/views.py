from datetime import datetime
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.db.models import Avg
from .models import *

# AGE ERROR 
class AgeValidationError(Exception):
    pass


# CALCULATE AGE FROM DOB 
def calculate_age(date_of_birth):
    today = datetime.today()
    dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def home(request):  # sourcery skip: extract-method
    error_message = None
    # Add Teacher, CREATE OPERATION
    if request.method == "POST":
        data = request.POST
        
        full_name = data.get("teacher_name")
        age = data.get("teacher_age")
        date_of_birth = data.get("teacher_dob")
        number_of_classes = data.get("teacher_number_of_classes")

        try:
            dob_age = calculate_age(date_of_birth)
            print(dob_age)
            if int(age) < 18:
                raise AgeValidationError("Age must be at least 18.")
            elif dob_age != int(age):
                raise AgeValidationError("Age is not same as per DOB.")
            Teacher.objects.create(
                full_name = full_name,
                age = age,
                date_of_birth = date_of_birth,
                number_of_classes = number_of_classes
            )
        except IntegrityError:
            error_message = "A teacher with this name and date of birth already exists."
        except ValueError:
            print('error occur')
            error_message = "Empty Fields are not allowed."
        except AgeValidationError as e:
            error_message = e
        except ValidationError as e:
            error_message = e.message

        
        if not error_message:
            return redirect('/')
    
    
    # Teachers Data, READ OPERATION
    queryset = Teacher.objects.all()
    
    # SEARCH TEACHER 
    if request.GET.get('search'):
        queryset = queryset.filter(full_name__icontains = request.GET.get('search'))
        
    # FILTER TEACHER BASED ON AGE AND NUMBER OF CLASSES
    elif request.GET.get('filter_age') or request.GET.get('filter_class'):
        filter_age = request.GET.get('filter_age', '').strip()
        filter_class = request.GET.get('filter_class', '').strip()
        
        if filter_age:
            age_queryset = queryset.filter(age__icontains=filter_age)
        else:
            age_queryset = queryset
        
        if filter_class:
            class_queryset = queryset.filter(number_of_classes__icontains=filter_class)
        else:
            class_queryset = queryset
            
        queryset = age_queryset & class_queryset
    
    # AVERAGE NUMBER OF CLASS, OPTIONAL TASK 
    avg_classes = queryset.aggregate(Avg('number_of_classes'))['number_of_classes__avg']
    if avg_classes is not None:
        avg_classes = round(avg_classes)
        
    context = {'teachers': queryset,
               'avg_classes': avg_classes,
               'error_message': error_message,
            }
    
    return render(request, "home/index.html", context)


# Delete Teacher, DELETE OPERATION
def delete_teacher(request, id):
    queryset = Teacher.objects.get(id = id)
    queryset.delete()
    return redirect('/')


# Update Teacher, UPDATE OPERATION
def update_teacher(request, id):  # sourcery skip: extract-method
    error_message = None
    queryset = Teacher.objects.get(id = id)

    if request.method == "POST":
        data = request.POST

        full_name = data.get("teacher_name")
        age = data.get("teacher_age")
        date_of_birth = data.get("teacher_dob")
        number_of_classes = data.get("teacher_number_of_classes")

        try:
            dob_age = calculate_age(date_of_birth)
            if int(age) < 18:
                raise AgeValidationError("Age must be at least 18.")
            elif dob_age != int(age):
                raise AgeValidationError("Age is not same as per DOB.")
            queryset.full_name = full_name
            queryset.age = age
            queryset.date_of_birth = date_of_birth
            queryset.number_of_classes = number_of_classes
            queryset.save()
        except IntegrityError:
            error_message = "A teacher with this name and date of birth already exists."
        except ValueError:
            error_message = "Empty Fields are not allowed."
        except AgeValidationError as e:
            error_message = e
        except ValidationError:
            error_message = "Empty Fields or wrong input are not allowed."
        
        if not error_message:
            return redirect('/')
        
    context = {'teacher': queryset, 'error_message': error_message}

    return render(request, "home/update.html", context)  