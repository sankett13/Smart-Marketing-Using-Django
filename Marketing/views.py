from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
# Create your views here.

# def index(request):
#     if request.method=="POST": 
#         redirect("index")
#     return render(request,"index.html")

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