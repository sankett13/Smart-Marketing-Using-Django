from django.urls import path
from . import views


urlpatterns = [
    path('',views.TestView.as_view(),name='index'),
    path('login',views.login_view,name='login'),
    # path('index/',views.index,name='index'),
]

