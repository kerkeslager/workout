from django.urls import path

from . import views

app_name = 'authorization'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('delete/', views.delete, name='delete'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
]
