from django.shortcuts import render,redirect
from django.http import JsonResponse
from datetime import datetime
from .models import todo
from django.contrib import messages
from django.core import serializers
import json
def index(request):
    data = todo.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        date = request.POST.get('date')
        # Convert date string to datetime object using the correct format
        if title and date:  # Check if title and date are not empty
            date_obj = datetime.strptime(date, "%d/%m/%Y")
            # Format the date object to 'YYYY-MM-DD'
            formatted_date = date_obj.strftime('%Y-%m-%d')

            todo.objects.create(title=title, due=formatted_date, status=0)
            messages.success(request, f'Todo "{title}" add successfully!')
        else:
            messages.error(request, f'All fields are required!')


    return render(request, "index.html",{'todo':data})
def getData(request,id):
    try:
        data = todo.objects.get(pk=id)
        if(request.method == 'POST'):
            title = request.POST.get('title')
            date = request.POST.get('date')
            if title and date:
                data.title = title
                data.due = date
                data.save()
                messages.success(request, f'Todo "{title}" updated successfully!')
            else:
                messages.error(request, f'All fields are required!')
            return redirect('/')
        else:
            serialized_data = serializers.serialize('json', [data])
            deserialized_data = json.loads(serialized_data)
            return JsonResponse({"data":deserialized_data, 'status':200})
    except todo.DoesNotExist:
        return JsonResponse({'message':'Todo does not exist.','status':404})
def delete(request,id):
    try:
        check = todo.objects.get(pk=id)
        title = check.title
        check.delete()
        messages.success(request, f'Todo "{title}" deleted successfully!')

    except todo.DoesNotExist:
        messages.error(request, 'Todo does not exist.')
    return redirect('/')
def changeStatus(request,id):
    try:
        check = todo.objects.get(pk=id)
        message = "completed"
        status = 1
        if(check.status == 1):
            status = 0
            message = "incomplete"
        check.status = status
        check.save()
        return JsonResponse({'message':f'Todo "{check.title}" converted to {message}  successfully!','status':200})
        # messages.success(request, f'Todo "{check.title}" converted to {message}  successfully!')

    except todo.DoesNotExist:
        return JsonResponse({'message':'Todo does not exist.','status':404})

 
    
