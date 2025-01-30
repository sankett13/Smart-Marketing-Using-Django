from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import User_info
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *

import os,sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from utils import get_groq_news

# Create your views here.

# def index(request):
#     if request.method=="GET":
#         return render(request,"index.html")
#     if request.method=="POST":
#         return redirect("TestView")

class TestView(APIView):
    def get(self,request,*args,**kwargs):
        us=User_info.objects.all()
        serializer=UserSerializer(us,many=True)
        return render (request,"index.html")
    
    def post(self,request,*args, **kwargs):
        if User_info.objects.filter(email=request.data["email"]).exists():
            return Response("Email already exists")
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
                #extraction of news for food
                prompt = """Find the latest food trends in Gujarat, India, for the current winter season. The response should be structured in news-style bullet points and cover the following aspects:


                - **Trending Seasonal Dishes** – Popular Gujarati winter foods gaining traction.
                - **New Food Industry Trends** – Any new restaurant concepts, fusion foods, or health-focused winter diets emerging in Gujarat.
                - **Street Food Innovations** – Any trending street food or winter-special snacks unique to Gujarat.                
                - **Beverage Trends** – Popular winter drinks, including herbal teas or immunity-boosting beverages.
                - **Health & Wellness Trends** – Any superfoods, organic, or plant-based trends popular in Gujarat this winter.
                - **Cultural Events** – Any cultural events, festivals, or celebrations unique to Gujarat this winter.
                - **Food Industry Updates** – New food startups, restaurant launches, or winter-themed food nonprofits happening in Gujarat.
                - **Travel Trends** – Popular winter destinations, accommodations, or activities in Gujarat.

                The response should be concise, factual, and up-to-date, ensuring all insights are specific to Gujarat and the winter season."""
                news = get_groq_news(prompt)
                #format this news
                print(news)

                return render(request,"dashboard.html",{"news":news})
        else:
            return HttpResponse("Invalid credentials")

    return render(request,"login.html")