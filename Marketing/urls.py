from django.urls import path
from . import views


urlpatterns = [
    path('',views.TestView.as_view(),name='index'),
    path('login',views.login_view,name='login'),
    # path('index/',views.index,name='index'),
    path('send_whatsapp_message/',views.send_whatsapp_message,name='send_whatsapp_message'),
    path('send_email_message/',views.send_email_message,name='send_email_message'),
]

