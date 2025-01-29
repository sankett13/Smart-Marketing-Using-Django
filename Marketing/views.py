from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

# Create your views here.

def index(request):
    if request.method=="POST":
        redirect("index")
    return render(request,"index.html")