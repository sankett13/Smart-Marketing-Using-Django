from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import User_info
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
import random
import json
from groq import Groq
# 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

#for WhastApp message
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# for groq api
import os,sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from utils import get_groq_news
import re


# for email
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

# def index(request):
#     if request.method=="GET":
#         return render(request,"index.html")
#     if request.method=="POST":
#         return redirect("TestView")

################################################## functions ################################################################
def send_email(email,subject,message):
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    













####################################################  Views ################################################################


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

                The response should be concise, factual, and up-to-date, ensuring all insights are specific to Gujarat and the winter season. All The Headings in the Response must be enclosed in html <h2> tags and all the Points in List tags"""
                news = get_groq_news(prompt)
                sections = news.strip().split("\n\n")
                news_dict = []
                for section in sections:
                    news_dict.append(section)
                    # print(section)
                request.session["news"]=news_dict
                # print(news_dict)

                return redirect("dashboard")
        else:
            return HttpResponse("Invalid credentials")
            

    return render(request,"login.html")





def send_whatsapp_message(request):
    if request.method == 'POST':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        users = User_info.objects.all()
        user_details = []
        for user in users:
            user_details.append({
                'name': user.name,
                'phone_number': user.phone_number,
            })
        
        driver.get("https://web.whatsapp.com/")
        input("Press Enter to continue after scanning QR code")
        # print(user_details)
        message = json.loads(request.body)["message"]
        print(message)
        for user in user_details:
            print(user.get('phone_number'))
            driver.get(f"https://web.whatsapp.com/send?phone={user.get('phone_number')}&text={message}")
            time.sleep(10)
            try:
                send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
                send_button.click()
                time.sleep(5)
                print(f"Message sent to {user.get('name')}")
            except Exception as e:
                print(e)

        driver.quit()
        return JsonResponse({"message": "Message sent successfully"}, status=200)
    return JsonResponse({"message": "Invalid request method"}, status=400)


def send_email_message(request):
    if request.method == 'POST':
        subject = "Test email"
        message = json.loads(request.body)["message"]
        users = User_info.objects.all()
        for user in users:
            print(user.email)
            send_email(user.email,subject,message)
            time.sleep(5)

        return JsonResponse({"message": "Email sent successfully"}, status=200)


    return HttpResponse("Email sent successfully")



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
    print("Hello World")
    news=request.session.get("news")
    return render(request,"dashboard.html",{"name":"sahal","news":news})

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
                    "content": text+"keep the title in h2 tag in html and content in list tag",
                },
                {
                    "role":"system",
                    "content":"you are a Food blog writer"
                }
            ],
            model="mixtral-8x7b-32768",
                )
            result=chat_completion.choices[0].message.content.strip()
            if result:
                # print(result)
                cleaned_result = re.sub(r'<think>.*?<\/think>', '', result, flags=re.DOTALL)
                print(cleaned_result)

                return JsonResponse({"content":cleaned_result})
            
        except Exception as er:
            print(er)
            return JsonResponse({"content":"Error"})

            
    else:
        return Response({"content":"Invalid Request Method"})
    


def get_news(request):
    prompt = """Find the latest food trends in Gujarat, India, for the current winter season. The response should be structured in news-style bullet points and cover the following aspects:


                - **Trending Seasonal Dishes** – Popular Gujarati winter foods gaining traction.
                - **New Food Industry Trends** – Any new restaurant concepts, fusion foods, or health-focused winter diets emerging in Gujarat.
                - **Street Food Innovations** – Any trending street food or winter-special snacks unique to Gujarat.                
                - **Beverage Trends** – Popular winter drinks, including herbal teas or immunity-boosting beverages.
                - **Health & Wellness Trends** – Any superfoods, organic, or plant-based trends popular in Gujarat this winter.
                - **Cultural Events** – Any cultural events, festivals, or celebrations unique to Gujarat this winter.
                - **Food Industry Updates** – New food startups, restaurant launches, or winter-themed food nonprofits happening in Gujarat.
                - **Travel Trends** – Popular winter destinations, accommodations, or activities in Gujarat.

                The response should be concise, factual, and up-to-date, ensuring all insights are specific to Gujarat and the winter season. All The Headings in the Response must be enclosed in html <h2> tags and all the Points in List tags"""
    news=get_groq_news(prompt)
    # print(news)
    return JsonResponse({"news":news,"status":200})
    
    