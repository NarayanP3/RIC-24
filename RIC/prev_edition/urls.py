from django.urls import path, reverse_lazy
from . import views


app_name='pre'
urlpatterns = [
   path('18', views.RC18.as_view(),name='rc18'),
   path('19', views.RC19.as_view(),name='rc19'),
   path('20', views.RC20.as_view(),name='rc20'),
]