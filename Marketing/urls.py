from django.urls import path
from . import views


urlpatterns = [
    path('',views.TestView.as_view(),name='index'),
    path('login/',views.login_view,name='login'),
    path("dashboard/<str:news>",views.dashboard,name="dashboard"),
    path("generate_result/",views.generate_result,name="generate_result"),
    path('send_whatsapp_message/',views.send_whatsapp_message,name='send_whatsapp_message'),
    path('send_email_message/',views.send_email_message,name='send_email_message'),
]

