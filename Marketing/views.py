from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import User_info
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from faker import Faker
from .serializer import *
import random
import json
from groq import Groq
# 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
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
                return redirect("dashboard")
        else:
            return HttpResponse("Invalid credentials")

    return render(request,"login.html")


def dashboard(request):
    # fake=Faker()
    # users=[]
    # for i in range(5):
    #     user=User_info.objects.create(
    #         name=fake.name(),
    #         email=fake.email(),
    #         phone_number=fake.phone_number(),
            
    #     )
    #     users.append(user)
    # categories=[]
    # for i in range(5):
    #     category=Category.objects.create(
    #         category_name=fake.word()
    #     )
    #     categories.append(category)
        
    # products=[]   
    # for i in range(10):
    #     product=Product.objects.create(
    #         product_name=fake.word(),
    #         category=random.choice(categories),
    #         price=round(random.uniform(10,1000),2),
    #         available_stock=random.randint(1,10),
            
    #     )
    #     products.append(product)
    # for i in range(20):
    #     user_history.objects.create(
    #         user_id=random.choice(users),
    #         product_id=random.choice(products),
    #         quantity=random.randint(1,10)
    #     )
    
    return render(request,"dashboard.html",{"name":"sahal"})

def generate_result(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body)
            text=data["prompt"]
            print(text)
            client = Groq(
            api_key="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"
            )
            # prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{article}\n\nArticle:"
            chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": text,
                },
                {
                    "role":"system",
                    "content":"You are an AI that will helps to search and Scrape News about Trends Regarding propular and traditional foods and drinks of the place asked during a specific season asked"
                }
            ],
            model="deepseek-r1-distill-llama-70b",
                )
            result=chat_completion.choices[0].message.content.strip()
            if result:
                return JsonResponse({"content":result})
            
        except Exception as er:
            print(er)
            return JsonResponse({"content":"Error"})

            
    else:
        return Response({"content":"Invalid Request Method"})