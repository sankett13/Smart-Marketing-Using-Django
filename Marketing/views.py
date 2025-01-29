from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.

def index(request):
    print("Demon1")
    return HttpResponse("Hello,Tenz Change!!")