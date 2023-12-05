from django.urls import path, include
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_, name='login'),
    path('personal/', views.personal, name='personal'),
    path('register/', views.register, name='register'),
    path('updateUser/', views.updateUser, name='updateUser'),
    path('updateRecord/<int:trackable_id>/', views.updateRecord, name='updateRecord')
]