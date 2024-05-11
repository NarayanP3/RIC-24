from django.urls import path, reverse_lazy
from . import views


app_name='dashboard'

urlpatterns = [

    path('send-preRIC/', views.send_instructions, name='send_preRIC'),

]