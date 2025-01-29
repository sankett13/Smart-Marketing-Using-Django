from django.urls import path
from . import views


urlpatterns = [
    path('api/',views.TestView.as_view(),name='index'),
    path('login',views.login_view,name='login'),
]

