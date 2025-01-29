from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import User_info
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
# Create your views here.

class TestView(APIView):
    def get(self,request,*args,**kwargs):
        us=User_info.objects.all()
        serializer=UserSerializer(us,many=True)
        return Response(serializer.data)
    
    def post(self,request,*args, **kwargs):
        us=User_info.objects.all()
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return render(request,"dashboard.html")
        else:
            return HttpResponse("Invalid credentials")

    return render(request,"login.html")