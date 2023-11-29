from django.urls import path, include
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_, name='login'),
    path('personal/', views.personal, name='personal'),
]