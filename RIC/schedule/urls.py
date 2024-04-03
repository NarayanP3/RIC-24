from django.urls import path, reverse_lazy
from . import views


app_name='schedule'
urlpatterns = [
    path('', views.ScheduleView.as_view(),name='all'),

]