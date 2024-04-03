from django.urls import path, reverse_lazy
from . import views


app_name='faq'
urlpatterns = [
   # path('', views.HomeView.as_view(),name='home'),
   path('', views.FAQList.as_view(),name='all'),
]