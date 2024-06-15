from django.shortcuts import render, redirect
from django.db.models import Avg
from .models import *


def home(request):
    # Add Teacher, CREATE OPERATION
    if request.method == "POST":
        data = request.POST
        
        full_name = data.get("teacher_name")
        age = data.get("teacher_age")
        date_of_birth = data.get("teacher_dob")
        number_of_classes = data.get("teacher_number_of_classes")
        
        Teacher.objects.create(
            full_name = full_name,
            age = age,
            date_of_birth = date_of_birth,
            number_of_classes = number_of_classes
        )
        
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
        
    context = {'teachers': queryset, 'avg_classes': avg_classes}
    
    return render(request, "home/index.html", context)


# Delete Teacher, DELETE OPERATION
def delete_teacher(request, id):
    queryset = Teacher.objects.get(id = id)
    queryset.delete()
    return redirect('/')


# Update Teacher, UPDATE OPERATION
def update_teacher(request, id):  # sourcery skip: extract-method
    queryset = Teacher.objects.get(id = id)

    if request.method == "POST":
        data = request.POST

        full_name = data.get("teacher_name")
        age = data.get("teacher_age")
        date_of_birth = data.get("teacher_dob")
        number_of_classes = data.get("teacher_number_of_classes")

        queryset.full_name = full_name
        queryset.age = age
        queryset.date_of_birth = date_of_birth
        queryset.number_of_classes = number_of_classes
        
        queryset.save()

        return redirect('/')
    context = {'teacher': queryset}

    return render(request, "home/update.html", context)  