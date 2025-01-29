from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.

def index(request):
    print("Tenz")
    return HttpResponse("Hello,Tenz Change!!")