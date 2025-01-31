from django.urls import path
from . import views


urlpatterns = [
    path('',views.TestView.as_view(),name='index'),
    path('login',views.login_view,name='login'),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("generate_result/",views.generate_result,name="generate_result"),
]

