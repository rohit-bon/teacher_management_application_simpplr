from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
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
    context = {'teachers' : queryset}
    
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